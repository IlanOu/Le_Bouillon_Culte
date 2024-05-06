import json
import random

from src.toolbox.Debug import Debug

from src.quiz.Quiz import Quiz

# Où c'est ?
# ---------------------------------------------------------------------------- #

class Quiz_OuCest(Quiz):
    def __init__(self, rfid_reader, json_path = ""):
        self.name = "Où c'est ?"
        self.json_path = json_path
        self.datas = {}
        self.fill_datas()
        self.rfid_reader = rfid_reader
    
    def fill_datas(self):
        if (self.json_path != ""):
            with open(self.json_path, 'r') as file:
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
