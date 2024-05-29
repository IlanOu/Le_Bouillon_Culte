import json
from src.quiz.Quiz import Quiz

from src.toolbox.Debug import Debug
from src.toolbox.Speaker import Speaker
from src.quiz.MusicPlayer import MusicPlayer

from src.Config import Config, ScoreConfig

import random
import time
import os

# Devine la suite 
# ---------------------------------------------------------------------------- #

class Quiz_DevineSuite(Quiz):
    def __init__(self, sensors_manager, json_path = ""):
        self.name = "Devine la suite"
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
        first_audio_value = question["audio-1"]
        second_audio_value = question["audio-2"]
        first_text_value = question["texte-1"]
        details_value = question["details"]
    
    
        # System
        # ---------------------------------------------------------------------------- #
        music_player = MusicPlayer(Config().audio_dir)

        text_mode = first_text_value != ''


        # 1. Display question
        Config().webApp.show(question_value, "text")
        Speaker.say(question_value.replace("/n", ""))

        if text_mode:
            Config().webApp.show(first_text_value, "text")
            Speaker.say(first_text_value)
        else:
            # Play Audio
            # full_audio_path = os.path.join(Config().audio_dir, first_audio_value)
            music_player.play(first_audio_value)
            
        
        # 2. Display responses
        Config().webApp.show(display_possible_responses_value, "table")
        Speaker.say(speakeable_possible_responses_value)
    
        # 3. Wait for response

        button_pin = self.sensors_manager.wait_for_button_press()

        if not button_pin in Config().buttons_pins:
            Debug.LogError("Il n'y a pas autant de bouton que de cases dans le tableau ! Il en faut 4 !")

        button_response = ScoreConfig().numbers_question[Config().buttons_pins.index(button_pin)]

        Debug.LogWhisper(f"Ma réponse est : {button_response} et la correct est {response_value}")




        # 5. Afficher la réponse + détails
        if button_response == response_value:
            response = "La bonne réponse était : " + response_value
            ScoreConfig().update_score("DevineSuite", True)
        else:
            response = "Dommage. La bonne réponse était : " + response_value
            ScoreConfig().update_score("DevineSuite", False)
        
        # 4. Display response
        Config().webApp.show("Bonne réponse : /n" + response_value + "/n" + details_value, "text")
        
        Speaker.say(response)
        
        time.sleep(3)
        Config().webApp.show("Bonne réponse : /n" + response_value + "/n" + details_value, "text")
        
        # Play Audio
        if text_mode:
            time.sleep(10)
        else:
            # full_audio_path = os.path.join(Config().audio_dir, second_audio_value)
            music_player.play(second_audio_value)
        
            time.sleep(3)

