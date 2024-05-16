import json
from src.quiz.Quiz import Quiz

from src.toolbox.Debug import Debug
from src.toolbox.Speaker import Speaker, GttsEngine

from src.Config import Config

import random
import time

# Qui suis-je ?
# ---------------------------------------------------------------------------- #

class Quiz_QuiSuisJe(Quiz):
    def __init__(self, sensors_manager, json_path = ""):
        self.name = "Qui suis-je ?"
        self.json_path = json_path
        self.datas = {}
        self.fill_datas()
        self.sensors_manager = sensors_manager
        

    def fill_datas(self):
        if (self.json_path != ""):
            with open(self.json_path, 'r') as file:
                self.datas = json.load(file)

    def get_random_question(self, zone=""):
        if self.datas == {}:
            Debug.LogError("Il n'y a pas de données dans le Json 'qui_suis_je.json'. Vérifiez le contenu du Json.")
            return None
        
        if zone == "" or not zone in self.datas:
            Debug.LogError("La zone est incorrectement définie pour le qui_suis_je.")
            Debug.LogWhisper("Vous pouvez mettre une zone avec : quiz.set_zone('zone').")
            return None
        
        random_question = random.choice(self.datas[zone])
        return random_question

    def process(self):
        question = self.get_random_question(Config().zone)
        
        # Get values
        # ---------------------------------------------------------------------------- #
        question_value = question["question"]
        possible_responses_value = random.sample(question["answers"], len(question["answers"]))
        speakeable_possible_responses_value = "\n - " + "\n - ".join(possible_responses_value).replace("/n", "")
        display_possible_responses_value = " | ".join(possible_responses_value)
        response_value = question["correct_answer"]
        details_value = question["details"]
        details_image_value = question["details_image"]

    
        # System
        # ---------------------------------------------------------------------------- #
        
        # 1. Display question
        Config().webApp.show(question_value, "text")
        Speaker.say(question_value.replace("/n", ""), GttsEngine())
        
        # 2.
        Config().webApp.show(display_possible_responses_value, "table")
        Speaker.say(speakeable_possible_responses_value, GttsEngine())
    
        # 3. Wait for response
        self.sensors_manager.wait_for_button_press()
        
        # 4. Display response
        response = "La bonne réponse était : " + response_value
        Config().webApp.show("Bonne réponse : /n" + response_value + "/n" + details_value, "text")
        
        Speaker.say(response, GttsEngine())
        
        time.sleep(3)
        Config().webApp.show("images/" + details_image_value, "image")
        
        time.sleep(10)
        
        
        