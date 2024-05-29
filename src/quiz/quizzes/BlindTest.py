import json
import random

from src.toolbox.Debug import Debug
from src.toolbox.Speaker import Speaker

from src.quiz.Quiz import Quiz
from src.quiz.MusicPlayer import MusicPlayer

from src.objects.displayer.WebDisplayer import *

from src.Config import Config, ScoreConfig


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
        speakeable_possible_responses_value = "\n - " + "\n - ".join(possible_responses_value)
        display_possible_responses_value = " | ".join(possible_responses_value)
        response_value = question["correct_answer"]
        audio_value = question["audio"]
        details_value = question["details"]
        
        
        # System
        # ---------------------------------------------------------------------------- #
        
        # 1. Poser la question
        Config().webApp.show(question_value, "text")
        Speaker.say(question_value)
        
        # 2. Passer la musique
        player = MusicPlayer(Config().audio_dir)
        music_file = audio_value
        player.play_random_section(music_file)
    
        # 3. Proposer les réponses
        Config().webApp.show(question_value + " ~ " + display_possible_responses_value, "table")
        Speaker.say(speakeable_possible_responses_value)
        
        # 4. Attendre la réponse de l'utilisateur
        button_pin = self.sensors_manager.wait_for_button_press()

        if not button_pin in Config().buttons_pins:
            Debug.LogError("Il n'y a pas autant de bouton que de cases dans le tableau ! Il en faut 4 !")

        button_response = possible_responses_value[Config().buttons_pins.index(button_pin)]
        
        
        # 5. Afficher la réponse + détails
        if button_response == response_value:
            response = "Bravo vous avez trouvé !"
            ScoreConfig().update_score("BlindTest", True)
        else:
            response = "Ce n’est pas la bonne réponse."
            ScoreConfig().update_score("BlindTest", False)

        
        Config().webApp.show(response + "/n La réponse correcte est : /n" + response_value, "text")
        Speaker.say(response)
        
        Config().webApp.show(details_value, "text")
        
        player.play_next_random_section()
        
        self.sensors_manager.wait_for_button_press()