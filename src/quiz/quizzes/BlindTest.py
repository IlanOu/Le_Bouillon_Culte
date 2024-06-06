import json
import random
import time

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
        self.name = "Retrouvez l’audio"
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
        # speakeable_possible_responses_value = "\n - " + "\n - ".join(possible_responses_value)
        # display_possible_responses_value = " | ".join(possible_responses_value)
        response_value = question["correct_answer"]
        audio_value = question["audio"]
        details_value = question["details"]
        
        
        # System
        # ---------------------------------------------------------------------------- #
        
        #? ---------------------------------------------------------------------------- #
        #?                               Display question                               #
        #? ---------------------------------------------------------------------------- #
        
        object = [{
                "type": "text",
                "content": question_value,
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
            }]
        
        Config().webApp.show(object)
        Speaker.say(question_value)
        
        player = MusicPlayer(Config().audio_dir)
        music_file = audio_value
        player.play_random_section(music_file)
    
        
        #? ---------------------------------------------------------------------------- #
        #?                                  Question                                    #
        #? ---------------------------------------------------------------------------- #
        
        object = [
            {
                "type": "score",
                "question": "Question " + str(ScoreConfig().nb_actual_question) + "/" + str(ScoreConfig().nb_question),
                "score": "Score : " + str(ScoreConfig().total_score) + "/" + str(ScoreConfig().nb_question),
                "style": []
            },
            {
                "type": "text",
                "content": question_value,
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
            },{
                "type": "table",
                "items": possible_responses_value,
                "style": []
            },{
                "type": "text",
                "content": "Utilisez les boutons pour choisir",
                "style": ["text-medium", "text-italic", "text-black"]
            }]
        
        # Afficher et dire la question
        Config().webApp.show(object)
        
        
        name = ["Réponse A", "Réponse B", "Réponse C", "Réponse D"]
        for item in possible_responses_value:
            Speaker.say(name[possible_responses_value.index(item)] + ". " + item)
            # time.sleep(0.25)
        
        
        
        #? ---------------------------------------------------------------------------- #
        #?                                   Réponse                                    #
        #? ---------------------------------------------------------------------------- #
        
        button_pin = self.sensors_manager.wait_for_button_press()
        
        if not button_pin in Config().buttons_pins:
            Debug.LogError("Il n'y a pas autant de bouton que de cases dans le tableau ! Il en faut 4 !")
        
        index_answer = Config().buttons_pins.index(button_pin)
        
        answer_value = possible_responses_value[index_answer]
        
        object = [{
                "type": "score",
                "question": "Question " + str(ScoreConfig().nb_actual_question) + "/" + str(ScoreConfig().nb_question),
                "score": "Score : " + str(ScoreConfig().total_score) + "/" + str(ScoreConfig().nb_question),
                "style": []
            },{
                "type": "text",
                "content": question_value,
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
            },{
                "type": "table",
                "items": possible_responses_value,
                "style": [],
                "answer": answer_value
            },{
                "type": "text",
                "content": "I",
                "style": ["text-medium", "text-white"]
            }]
        
        Config().webApp.show(object)
        
        button_response = possible_responses_value[Config().buttons_pins.index(button_pin)]
        
        time.sleep(3)
        
        if button_response == response_value:
            response = random.choice(["Bien joué ! vous avez trouvé la bonne réponse !", "Félicitations, c’est la bonne réponse!", "C'est gagné !"])
            ScoreConfig().update_score("BlindTest", True)
        else:
            response = random.choice(["C’est raté !", "Malheureusement, ce n'est pas la bonne réponse", "C'est perdu !"])
            ScoreConfig().update_score("BlindTest", False)
        
        
        #? ---------------------------------------------------------------------------- #
        #?                            Affichage réponse - 1                             #
        #? ---------------------------------------------------------------------------- #
        object = [{
                "type": "score",
                "question": "Question " + str(ScoreConfig().nb_actual_question) + "/" + str(ScoreConfig().nb_question),
                "score": "Score : " + str(ScoreConfig().total_score) + "/" + str(ScoreConfig().nb_question),
                "style": []
            },{
                "type": "text",
                "content": response,
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
        }]
        
        Config().webApp.show(object)
        Speaker.say(response)
        
        time.sleep(3)
        
        
        #? ---------------------------------------------------------------------------- #
        #?                            Affichage réponse - 2                             #
        #? ---------------------------------------------------------------------------- #
        
        answer_value = "La bonne réponse était : \n" + response_value
        
        object = [{
                "type": "score",
                "question": "Question " + str(ScoreConfig().nb_actual_question) + "/" + str(ScoreConfig().nb_question),
                "score": "Score : " + str(ScoreConfig().total_score) + "/" + str(ScoreConfig().nb_question),
                "style": []
            },{
                "type": "text",
                "content": answer_value,
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
            },
            {
                "type": "text",
                "content": details_value,
                "style": ["text-medium", "text-uppercase", "text-blue", "text-bold-700", "text-centered"]
            }]
        
        Config().webApp.show(object)
        
        Speaker.say(answer_value)
        
        player.play_next_random_section()