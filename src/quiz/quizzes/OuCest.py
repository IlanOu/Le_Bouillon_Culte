import json
from src.quiz.Quiz import Quiz

from src.toolbox.Debug import Debug
from src.toolbox.Speaker import Speaker

from src.Config import Config

import random
import time


# Où c'est ?
# ---------------------------------------------------------------------------- #

class Quiz_OuCest(Quiz):
    def __init__(self, sensors_manager, json_path = ""):
        self.name = "Où c'est ?"
        self.json_path = json_path
        self.datas = {}
        self.fill_datas()
        self.sensors_manager = sensors_manager
    
    def fill_datas(self):
        if (self.json_path != ""):
            with open(self.json_path, 'r') as file:
                self.datas = json.load(file)


    def get_random_question(self):
        if self.datas == {}:
            Debug.LogError("Il n'y a pas de données dans le Json 'ou_cest.json'. Vérifiez le contenu du Json.")
            return None
        
        zone = random.choice(list(self.datas.keys()))
        
        random_question = random.choice(self.datas[zone])
        return random_question



    def process(self):
        question = self.get_random_question()
        
        # Get values
        # ---------------------------------------------------------------------------- #
        question_value = question["question"]
        answer_value = question["answers"]
        # speakeable_possible_responses_value = "\n - " + "\n - ".join(possible_responses_value).replace("/n", "")
        # display_possible_responses_value = " | ".join(possible_responses_value)
        response_value = Config().zone
        details_value = question["details"]

    
        # System
        # ---------------------------------------------------------------------------- #
        
        # 1. Display question
        Config().webApp.show("Où se trouve " + question_value, "text")
        Speaker.say("Où se trouve : ")
        Speaker.say(question_value.replace("/n", ""))
        
        # 2.
        Config().webApp.show(answer_value, "text")
        Speaker.say(answer_value)
    
        # 3. Wait for RFID # TODO -> Obtenir la position grâce aux différents capteurs RFID
        self.sensors_manager.read_rfid()
        
        # 4. Display response
        response = "La bonne réponse était : " + response_value
        Config().webApp.show("Bonne réponse : /n" + response_value + "/n" + details_value, "text")
        
        Speaker.say(response)
        
        time.sleep(10)