import json
import random

class Quiz:
    def __init__(self, json_file=""):
        self.json_file = json_file
        self.questions = ["Salut, comment vons-je ?", "Je suis un lapin ?"]
        self.responses = ["Eu, okay", "Non merci"]
        
        if (json_file != ""):
            self.fill_questions()
            self.fill_responses()

    def fill_questions(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            self.questions = data.get('question', [])

    def fill_responses(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            self.responses = data.get('answers', [])

    def get_random_question(self):
        return random.choice(self.questions)

    def get_random_response(self):
        return random.choice(self.responses)