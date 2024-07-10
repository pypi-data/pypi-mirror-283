import dspy


class AssessYesNo(dspy.Signature):
    """Assess the quality of a short description along the specified dimension."""
    assessed_text = dspy.InputField()
    assessment_context = dspy.InputField()
    assessment_answer = dspy.OutputField(desc="Yes or No")


class AssessLikert(dspy.Signature):
    """Assess the quality of a short description along the specified dimension."""
    assessed_text = dspy.InputField()
    assessment_context = dspy.InputField()
    assessment_answer = dspy.OutputField(desc="Number in range 1-10, where 1 is not at all similar and 10 is very "
                                              "similar")
