import json
import random

from src.toolbox.Debug import Debug
from src.toolbox.Speaker import *

from src.quiz.Quiz import Quiz
from src.quiz.MusicPlayer import MusicPlayer

from src.objects.displayer.WebDisplayer import *

from src.Config import Config


# Blind test 
# ---------------------------------------------------------------------------- #

class Quiz_BlindTest(Quiz):
    def __init__(self, sensors_manager, json_path = ""):
        self.json_path = json_path
        self.datas = {}
        self.name = "Blind test"
        self.fill_datas()
        self.sensors_manager = sensors_manager
        
        
    def fill_datas(self):
        if (self.json_path != ""):
            with open(self.json_path, 'r') as file:
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
        question = self.get_random_question(Config().zone)
        
        
        # Get values
        # ---------------------------------------------------------------------------- #
        question_value = question["question"]
        possible_responses_value = random.sample(question["answers"], len(question["answers"]))
        print(question["answers"])
        print(possible_responses_value)
        # print(random.shuffle(question["answers"]))
        speakeable_possible_responses_value = "\n - " + "\n - ".join(possible_responses_value)
        display_possible_responses_value = " | ".join(possible_responses_value)
        response_value = question["correct_answer"]
        audio_value = question["audio"]
        details_value = question["details"]
        
        
        # System
        # ---------------------------------------------------------------------------- #
        
        # 1. Poser la question
        Config().webApp.show(question_value, "text")
        Speaker.say(question_value, GttsEngine())
        
        # 2. Passer la musique
        player = MusicPlayer(Config().audio_dir)
        music_file = audio_value
        player.play_random_section(music_file)
    
        # 3. Proposer les réponses
        Config().webApp.show(question_value + " ~ " + display_possible_responses_value, "table")
        Speaker.say(speakeable_possible_responses_value, GttsEngine())
        
        # 4. Attendre la réponse de l'utilisateur
        button_pin = self.sensors_manager.wait_for_button_press()

        print("Le pin : " + str(button_pin) + " type : " + str(type(button_pin)))

        if button_pin == 16 :
            print("Réponse 1")
            buttonResponse = possible_responses_value[0]
        elif button_pin == 23 :
            print("Réponse 2")
            buttonResponse = possible_responses_value[1]
        elif button_pin == 26 :
            print("Réponse 3")
            buttonResponse = possible_responses_value[2]
        elif button_pin == 17 :
            print("Réponse 4")
            buttonResponse = possible_responses_value[3]

        print(f"Ma réponse est : {buttonResponse} et la correct est {response_value}")
        # 5. Afficher la réponse + détails
        if buttonResponse == response_value:
            response = "La bonne réponse était : " + response_value
        else:
            response = "Dommage. La bonne réponse était : " + response_value


        Config().webApp.show("Bonne réponse : /n" + response_value + "/n" + details_value, "text")
        Speaker.say(response, GttsEngine())
        player.play_next_random_section()
        