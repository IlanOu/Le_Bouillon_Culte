import json
from src.quiz.Quiz import Quiz


# Quiz F
# ---------------------------------------------------------------------------- #

class QuizF(Quiz):
    def __init__(self, rfid_reader, json_path = ""):
        self.name = "QuizF"
        self.json_path = json_path
        self.datas = {}
        self.fill_datas()
        self.rfid_reader = rfid_reader

    def fill_datas(self):
        if (self.json_path != ""):
            with open(self.json_path, 'r') as file:
                self.datas = json.load(file)

    def get_random_question(self, zone):
        # Implémentation spécifique pour QuizB
        pass

    def process(self):
        pass

