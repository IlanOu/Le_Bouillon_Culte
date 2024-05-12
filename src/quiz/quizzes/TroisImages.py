import json
from src.quiz.Quiz import Quiz


# Quiz F
# ---------------------------------------------------------------------------- #

class QuizF(Quiz):
    def __init__(self, sensors_manager, json_path = ""):
        self.name = "QuizF"
        self.json_path = json_path
        self.datas = {}
        self.fill_datas()
        self.sensors_manager = sensors_manager

    def fill_datas(self):
        if (self.json_path != ""):
            with open(self.json_path, 'r') as file:
                self.datas = json.load(file)

    def get_random_question(self, zone):
        # Implémentation spécifique pour QuizB
        pass

    def process(self):
        pass

