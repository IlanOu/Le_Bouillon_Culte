import json
from src.quiz.Quiz import Quiz

# Qui suis-je ?
# ---------------------------------------------------------------------------- #

class Quiz_QuiSuisJe(Quiz):
    def __init__(self, jsonPath = ""):
        self.name = "Qui suis-je ?"
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
