import json
import os

import dspy

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from dspy.teleprompt import BootstrapFewShotWithRandomSearch, BootstrapFinetune

from <package_name>.src.shared.models import AzureOpenAIClient, AzureOpenAILM, DART
from <package_name>.src.shared.metrics import AssessYesNo


def __extract_short_description(incident_str):
    str_lines = incident_str.splitlines()
    short_description, flag = '', False
    for line in str_lines:
        if 'A case was opened with a short description of' in line:
            flag = True
            line = line.split('A case was opened with a short description of')[1]
        elif 'A longer description includes' in line:
            break
        if flag:
            short_description += line
    return short_description


# Read Input Data:
def read_input_data(input_fpath):
    # Read the input data
    input_df = pd.read_excel(input_fpath)
    # Role and Problem Statement Extraction
    task_and_problem_extraction_prompt = '''Given the above incident, identify the subject/topic of the incident. 
    What is the person trying to accomplish, or the problem they're facing? Provide a description, and the context in which they're facing the issue.
    What is the role description of the person who opened the incident? If unclear or not provided, go ahead and generate a job description that can have the identified issue/question. 
    Give the output as a JSON object with the following keys: "subject" and "role". Return only the valid serialized JSON, and do not add markdown.'''
    # Check if Cache exists, and load. Else, call the API and save the cache.
    azure_openai = AzureOpenAIClient()
    input_df_cache = program_prefix + 'subject_and_role_cache.json'
    if not os.path.isfile(input_df_cache):
        input_df['subject_and_role'] = input_df['Context'].progress_apply(
            lambda x: azure_openai.call(azure_openai.generate_prompt_incident(x, task_and_problem_extraction_prompt)))
        input_df.to_json(input_df_cache)
    else:
        input_df = pd.read_json(input_df_cache)
    # Extract Subject, Roles and Golden Short Descriptions
    inputs_labels_sd = []
    for index, row in input_df.iterrows():
        try:
            data = json.loads(row['subject_and_role'])
            golden_sd = __extract_short_description(row['Context'])
            inputs_labels_sd.append((data['subject'], data['role'], golden_sd))
        except Exception as ex:
            print("Failed to extract Subject, Role or generate Short Description with Error: ", ex)
            print(row['subject_and_role'])
    # Return the Prepared Dataset
    return input_df, inputs_labels_sd


# Prepare DSPy Dataset
def prepare_short_description_dataset(input_fpath):
    input_df, inputs_labels = read_input_data(input_fpath)
    dataset = []
    for subject, role, short_description in inputs_labels:
        if (not subject or subject == 'UNKNOWN') or (not role or role == 'UNKNOWN') or not short_description:
            continue
        dataset.append(dspy.Example(subject=subject, role=role, short_description=short_description).with_inputs("subject", "role"))
    return dataset


# DSPy Program Definition (Short Description):
class ShortDescriptionSynth(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program = dspy.ChainOfThought("subject, role -> short_description")

    def forward(self, subject, role):
        return self.program(subject=subject, role=role)


class GenerateShortDescription:
    def __init__(self):
        # Configure
        self.azure_openai = AzureOpenAIClient()
        self.target_lm = DART()
        self.judge_lm = AzureOpenAILM()
        self.train_test_ratio = 0.9
        self.dataset_dev = None
        self.compiled_program = None

        dspy.settings.configure(lm=self.target_lm)

    def custom_short_desc_metric(self, gold, pred):
        subject, role, gold_short_desc, pred_short_desc = gold['subject'], gold['role'], gold['short_description'], \
            pred['short_description']
        try:
            good_short_desc, similarity, score = "", "", 0.0
            while score == 0:
                with dspy.context(lm=self.target_lm):
                    good_short_desc = dspy.Predict(AssessYesNo)(assessed_text=pred_short_desc,
                                                                assessment_context=f"Subject: {subject}\n\nRole: {role}")
                is_good_short_desc = good_short_desc.assessment_answer.lower().find('yes') >= 0
                #### Similarity Score using Embeddings
                similarity_score = \
                    cosine_similarity(np.array(self.azure_openai.get_embedding(gold_short_desc)).reshape(1, -1),
                                      np.array(self.azure_openai.get_embedding(pred_short_desc)).reshape(1, -1))[0][0]
                ####
                score = (is_good_short_desc / 1.0 + similarity_score / 1.0) / 2.0
            return score
        except Exception as ex:
            print(subject, role, gold_short_desc, pred_short_desc)
            print(ex)
            print(good_short_desc)
        return 0.0

    def train(self, dataset):
        dataset_train, self.dataset_dev = dataset[:int(self.train_test_ratio*len(dataset))], dataset[int(self.train_test_ratio*len(dataset)):]
        config = dict(max_bootstrapped_demos=4, max_labeled_demos=4)
        teleprompter = BootstrapFewShotWithRandomSearch(metric=self.custom_short_desc_metric, **config)
        self.compiled_program = teleprompter.compile(ShortDescriptionSynth(), trainset=dataset_train)
        return self.compiled_program

    def evaluate(self):
        evaluator = dspy.Evaluate(devset=self.dataset_dev, metric=self.custom_short_desc_metric, num_threads=4, display_progress=True, display_table=0)
        print(evaluator(self.compiled_program))

    def inspect_history(self):
        for item in self.target_lm.history:
            print(item)
            print("\n\n")

    def save(self, fpath):
        self.compiled_program.save(fpath)


def __init__():
    global program_prefix

    # Variables
    program_prefix = "inc_sd_"
    input_data_fpath = '/Users/venkatesh.gunda/Code/Research/DataSynth/incident_data.xlsx'
    compiled_program_fpath = '/Users/venkatesh.gunda/Code/Research/DataSynth/incident_table_program.dspy'

    # Prepare Dataset
    short_desc_dataset = prepare_short_description_dataset(input_data_fpath)

    # Initialize Trainer
    sd_gen_trainer = GenerateShortDescription()

    # Train the Program
    sd_gen_trainer.train(short_desc_dataset)

    # Evaluate the Program
    sd_gen_trainer.evaluate()

    # Save the Program
    sd_gen_trainer.save(compiled_program_fpath)
