import json
import random

from src.toolbox.Debug import Debug
from src.toolbox.Speaker import *

from src.quiz.MusicPlayer import MusicPlayer

from src.objects.Displayer.WebDisplayer import *
from src.objects.rfid.RFIDReader import RFIDReader




Debug.prefixActive = False


# ------------------------------- Quiz protocol ------------------------------ #

class Quiz:
    def __init__(self, jsonPath=""):
        self.name=""
        self.jsonPath = jsonPath
        self.datas = {}

    def process(self):
        Debug.LogError("La méthode get_random_question doit être implémentée dans les classes dérivées.")




# ---------------------------------- Quizzes --------------------------------- #





# Quiz F
# ---------------------------------------------------------------------------- #

class QuizF(Quiz):
    def __init__(self, jsonPath = ""):
        self.name = "QuizF"
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



# ------------------------------- Quiz manager ------------------------------- #


class QuizManager:
    def __init__(self):
        self.quizzes = []
        self.current_quiz = None
        self.zone = ""

    def set_zone(self, zone):
        self.zone = zone

    def add_quiz(self, quiz: Quiz):
        self.quizzes.append(quiz)
        
    def get_random_quiz(self):
        random_quiz = random.choice(self.quizzes)
        return random_quiz

    def set_current_quiz(self, quiz: Quiz):
        self.current_quiz = quiz


    def run(self):
        if self.current_quiz == None:
            Debug.LogError("Définissez d'abord le quiz ! [ Utilisez set_quiz() ]")
        # question = self.current_quiz.get_random_question(self.zone)
        try:
            self.current_quiz.process()
        except KeyboardInterrupt:
            Debug.LogSuccess("Programme interrompu par l'utilisateur")





# # Exemple d'utilisation
# ---------------------------------------------------------------------------- #
# manager = QuizManager()
# quiz1 = QuizA("quiz1.json")
# quiz2 = QuizB("quiz2.json")
# # Ajoutez les autres instances de quiz
# manager.add_quiz(quiz1)
# manager.add_quiz(quiz2)
# manager.run()