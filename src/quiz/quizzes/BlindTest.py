import json
import random

from src.toolbox.Debug import Debug
from src.toolbox.Speaker import *

from src.quiz.MusicPlayer import MusicPlayer

from src.objects.Displayer.WebDisplayer import *
# from src.objects.rfid.RFIDReader import RFIDReader

from src.quiz.Quiz import Quiz


# Blind test 
# ---------------------------------------------------------------------------- #

class Quiz_BlindTest(Quiz):
    def __init__(self, rfid_reader, json_path = ""):
        self.json_path = json_path
        self.datas = {}
        self.name = "Blind test"
        self.fill_datas()
        self.rfid_reader = rfid_reader
        
        
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
        # Exemple d'utilisation
        music_dir = "./assets/musics/"
        player = MusicPlayer(music_dir)
        music_file = audio_value
        player.play_random_section(music_file)
        
        
    
        # 3.
        webApp.show(question_value + " ~ " + display_possible_responses_value)
        Speaker.say(speakeable_possible_responses_value, GttsEngine())
        
        # 4.
        # pass
        self.rfid_reader.wait_for_button_press()
        
        # 5.
        response = "La bonne réponse était : " + response_value
        webApp.show("Bonne réponse : /n" + response_value + "/n" + details_value)
        Speaker.say(response, GttsEngine())
        # Speaker.say(details_value, GttsEngine())
        player.play_next_random_section()
        
        
        """ 
        1. Poser la question
        2. Passer la musique
        3. Proposer les réponses
        4. Attendre la réponse de l'utilisateur
        5. Afficher la réponse + détails
        """
        