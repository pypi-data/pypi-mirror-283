import json
import requests

from dspy import LM
from openai import OpenAI, AzureOpenAI

# Suppress InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class AzureOpenAIClient:
    def __init__(self, azure_endpoint="https://test-atg-openai.openai.azure.com/",
                 api_key="bcea2612fb0e40c88c3c06289b2c7d70", model_name='gpt-4o', api_version='2024-02-15-preview'):
        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.azure_base_url = f"{azure_endpoint}/openai/deployments"
        self.api_key = api_key
        self.model_name = model_name
        self.api_version = api_version
        self.system_prompt = '''Be honest, truthful, accurate and concise. If the requested information is not 
        present or the answer is unclear, reply with "UNKNOWN".'''

    def call(self, prompt, model_name='', api_version='', system_prompt=''):
        model_name = model_name if model_name else self.model_name
        api_version = api_version if api_version else self.api_version
        system_prompt = system_prompt if system_prompt else self.system_prompt
        if "gpt-4o" in model_name:  # Multi-Modal Model (GPT-4o)
            message_text = [{"role": "system", "content": [{"type": "text", "text": system_prompt}]},
                            {"role": "user", "content": [{"type": "text", "text": prompt}]}]
        else:
            message_text = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
        headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }
        payload = {
            "messages": message_text,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        url = f"{self.azure_base_url}/{model_name}/chat/completions?api-version={api_version}"
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            output = response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as ex:
            raise Exception(f"Error calling OpenAI model: {ex}")
        return output

    def get_embedding(self, text, model_name="text-embedding-3-large"):
        response = self.client.embeddings.create(
            input=text,
            model=model_name
        )
        return response.data[0].embedding

    @staticmethod
    def generate_prompt_incident(incident, instruction):
        incident_prompt_template = '''INCIDENT DETAILS:\n{incident}\n\n\nINSTRUCTION:\n{instruction}'''
        return incident_prompt_template.format(incident=incident, instruction=instruction)


class NGC(LM):
    kwargs = {
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 1024,
        "stream": False
    }

    def __init__(self, system_prompt=''):
        self.provider = "default"
        self.history = []
        self.system_prompt = system_prompt
        self.kwargs = {
            "temperature": 0.5,
            "top_p": 1,
            "max_tokens": 1024,
            "stream": False
        }

    def get_model_response(self, prompt):
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key="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"
            # "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"
        )
        completion = client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct-v0.1",
            messages=prompt,
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=False
        )
        return completion

    def basic_request(self, prompt, **kwargs):
        messages = [
            {
                "role": "system",
                "content": (
                               self.system_prompt + "\n\n" if self.system_prompt else "You are a helpful agent who "
                                                                                      "helps users with their "
                                                                                      "questions.") + (
                               kwargs["context"] if "context" in kwargs else "")
            },
            {
                "role": "user",
                "content": prompt  # aka instruction
            }
        ]
        response = self.get_model_response(messages)

        self.history.append({
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs
        })
        return response

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response = self.request(prompt, **kwargs)
        completions = [result.message.content for result in response.choices]
        return completions


class AzureOpenAILM(LM):
    kwargs = {
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 1024,
        "stream": False
    }

    def __init__(self, system_prompt=''):
        self.provider = "default"
        self.history = []
        self.system_prompt = system_prompt
        self.kwargs = {
            "temperature": 0.5,
            "top_p": 1,
            "max_tokens": 1024,
            "stream": False
        }
        self.model_client = AzureOpenAIClient()

    def get_model_response(self, prompt):
        return self.model_client.call(prompt, system_prompt=self.system_prompt)

    def basic_request(self, prompt, **kwargs):
        response = self.get_model_response(prompt)
        self.history.append({
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs
        })
        return response

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response = self.request(prompt, **kwargs)
        # completions = [result.message.content for result in response.choices]
        return [response]


class DART(LM):
    kwargs = {
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 1024,
        "stream": False
    }

    def __init__(self, system_prompt=''):
        self.provider = "default"
        self.history = []
        self.system_prompt = system_prompt
        self.kwargs = {
            "temperature": 0.5,
            "top_p": 1,
            "max_tokens": 1024,
            "stream": False
        }

    def get_model_response(self, prompt):
        url = 'https://mlprediction-dart-main-dart002.bwi100.service-now.com/v2/models/llm_generic/infer'
        options = {"max_tokens": 500, "temperature": 0.8, "top_k": 1, "top_p": 0.0, "num_beams": 1}
        options = json.dumps(options)
        headers = {
            'Content-Type': 'application/json'
        }
        verify = False
        payload = json.dumps({
            "id": "42",
            "inputs": [{
                    "name": "request",
                    "shape": [1, 1],
                    "datatype": "BYTES",
                    "data": [prompt]
                }, {
                    "name": "options",
                    "shape": [1, 1],
                    "datatype": "BYTES",
                    "data": [
                        options
                    ]
                }, {
                    "name": "request_metadata",
                    "shape": [1, 1],
                    "datatype": "BYTES",
                    "data": [
                        "{\"trace_id\":\"12hhsi34kllmgen1\"}"
                    ]
                }
            ],
            "outputs": [{
                    "name": "response"
                }, {
                    "name": "error"
                }, {
                    "name": "response_metadata"
                }
            ]
        })

        response = requests.request("POST", url, headers=headers, data=payload, verify=verify)
        model_output = ''
        try:
            response_data = json.loads(response.text).get('outputs')[0].get('data')[0]
            model_output = json.loads(response_data)['model_output']
        except Exception as e:
            print(f"Exception: {e}")
            print(json.loads(response.text))
            return model_output
        return model_output

    def basic_request(self, prompt, **kwargs):
        messages = '<s>[INST]' + (
            self.system_prompt if self.system_prompt else "You are a helpful agent who helps users with their "
                                                          "questions, but also lets them know if you don't know the "
                                                          "answer.") + '\n\n' + prompt + '[/INST]'
        response = self.get_model_response(messages)

        self.history.append({
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs
        })
        return response

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response = self.request(prompt, **kwargs)
        return [response.replace('</s>', '')]
