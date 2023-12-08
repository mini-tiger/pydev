from dataclasses import dataclass


class PromptQA:
    # vaild: bool = False
    # prompt: str
    # question_std: str
    # answers_std: str
    # answers_real: str
    def __init__(self):
        self.question_std = ""
        self.answers_std = ""
        self.answers_real = ""
        self.valid = False
        self.prompt = ""
        self.prompt_gpt_source = ""
        self.prompt_gpt = ""
        self.vec_score = 0
        self.rouge_score = 0
        self.err="not run"
        self.type=""
        self.time=0

    def put_data(self, valid=False, question_std="", answers_std="", answers_real=""):
        self.question_std = question_std
        self.answers_std = answers_std
        self.answers_real = answers_real
        self.valid = valid

    def put_prompt(self, prompt):
        self.prompt = prompt
