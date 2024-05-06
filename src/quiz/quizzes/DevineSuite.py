import json
from src.quiz.Quiz import Quiz

# Devine la suite 
# ---------------------------------------------------------------------------- #

class Quiz_DevineSuite(Quiz):
    def __init__(self, jsonPath = ""):
        self.name = "Devine la suite"
        self.jsonPath = jsonPath
        self.datas = {}
        self.fill_datas()

    def fill_datas(self):
        if (self.jsonPath != ""):
            with open(self.jsonPath, 'r') as file:
                self.datas = json.load(file)

    def get_random_question(self, zone):
        # Implémentation spécifique pour QuizB
        pass

    def process(self):
        pass

