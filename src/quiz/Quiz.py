import json
import random
from src.toolbox.Debug import Debug
from src.toolbox.Speaker import *

from src.objects.Displayer.WebDisplayer import *


Debug.prefixActive = False


# Quiz protocol
# ---------------------------------------------------------------------------- #

class Quiz:
    def __init__(self, jsonPath=""):
        self.name=""
        self.jsonPath = jsonPath
        self.datas = {}

    def process(self):
        Debug.LogError("La méthode get_random_question doit être implémentée dans les classes dérivées.")





# Quizzes
# ---------------------------------------------------------------------------- #

class Quiz_BlindTest(Quiz):
    def __init__(self, jsonPath = ""):
        self.jsonPath = jsonPath
        self.datas = {}
        self.name = "Blind test"
        self.fill_datas()
        
        
    def fill_datas(self):
        if (self.jsonPath != ""):
            with open(self.jsonPath, 'r') as file:
                self.datas = json.load(file)


    def get_random_question(self, zone=""):
        if self.datas == {}:
            Debug.LogError("Il n'y a pas de données dans le Json 'blind_test.json'. Vérifiez le contenu du Json.")
            return None
        
        if zone == "" or not zone in self.datas:
            Debug.LogError("La zone est incorrectement définie pour le blind_test.")
            Debug.LogWhisper("Vous pouvez mettre une zone avec : quiz.set_zone('zone').")
            return None
        
        random_question = random.choice(self.datas[zone])
        return random_question
    
    
    def process(self):
        zone = "Auvergne-Rhônes-Alpes" # Todo -> à changer plus tard en récupérant via les étapes précédentes dans l'Enum
        question = self.get_random_question(zone)
        
        
        # Get values
        question_value = question["question"]
        possible_responses_value = question["answers"]
        speakeable_possible_responses_value = "\n - " + "\n - ".join(possible_responses_value)
        display_possible_responses_value = " | ".join(possible_responses_value)
        response_value = question["correct_answer"]
        audio_value = question["audio"]
        details_value = question["details"]
        
        # 1.
        
        # Initialisation et exécution de l'application
        webApp = WebApp(update_interval=1)

        webApp.show(question_value)
        Speaker.say(question_value, GttsEngine())
        
        # 2.
        pass
    
        # 3.
        webApp.show(question_value + " ~ " + display_possible_responses_value)
        Speaker.say(speakeable_possible_responses_value, GttsEngine())
        
        # 4.
        pass
        
        # 5.
        response = "La bonne réponse était : " + response_value
        webApp.show("Bonne réponse : /n" + response_value + "/n" + details_value)
        Speaker.say(response, GttsEngine())
        Speaker.say(details_value, GttsEngine())
        
        
        """ 
        1. Poser la question
        2. Passer la musique
        3. Proposer les réponses
        4. Attendre la réponse de l'utilisateur
        5. Afficher la réponse + détails
        """
        



class Quiz_OuCest(Quiz):
    def __init__(self, jsonPath = ""):
        self.name = "Où c'est ?"
        self.jsonPath = jsonPath
        self.datas = {}
        self.fill_datas()
    
    def fill_datas(self):
        if (self.jsonPath != ""):
            with open(self.jsonPath, 'r') as file:
                self.datas = json.load(file)


    def get_random_question(self, zone=""):
        if self.datas == {}:
            Debug.LogError("Il n'y a pas de données dans le Json 'ou_cest.json'. Vérifiez le contenu du Json.")
            return None
        
        if zone == "" or not zone in self.datas:
            Debug.LogError("La zone est incorrectement définie pour le ou_cest.")
            Debug.LogWhisper("Vous pouvez mettre une zone avec : quiz.set_zone('zone').")
            return None
        
        random_question = random.choice(self.datas[zone])
        return random_question



    def process(self):
        zone = "Auvergne-Rhônes-Alpes" #TODO -> à changer plus tard en récupérant via les étapes précédentes dans l'Enum
        question = self.get_random_question(zone)
        
        question_value = question["question"]
        image_value = question["image"]
        response_value = zone
        hint_value = question["answers"]
        details_value = question["details"]

        """
        1. Dire les consignes "Vous devez placer le pion au bon endroit"
        2. Poser la question "Où se trouve, " + question_value
        3. Vérifier si le pion est placé au bon endroit sur la carte.
           S'il n'est pas placé, dire -> hint_value.
        4. Afficher la response_value + details_value
        """

        Debug.Log(question)



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



class Quiz_CultureG(Quiz):
    def __init__(self, jsonPath = ""):
        self.name = "Culture générale"
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



# Quiz manager
# ---------------------------------------------------------------------------- #

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
        self.current_quiz.process()





# # Exemple d'utilisation
# ---------------------------------------------------------------------------- #
# manager = QuizManager()
# quiz1 = QuizA("quiz1.json")
# quiz2 = QuizB("quiz2.json")
# # Ajoutez les autres instances de quiz
# manager.add_quiz(quiz1)
# manager.add_quiz(quiz2)
# manager.run()