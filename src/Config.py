from src.toolbox.Singleton import singleton
from src.toolbox.Debug import Debug
from src.toolbox.Speaker import *

@singleton
class Config:
    def __init__(self):
        # Can be changed
        # ---------------------------------------------------------------------------- #
        self.checker_active = False
        self.use_ESP_connection = False # set it to True
        
        self.test_mode = False
        
        Debug.prefixActive = False
        
        self.zone = "Auvergne-Rhône-Alpes"
        self.internal_RFID_zone = "Hauts-de-France"
        
        self.time_before_sleep = 20 # Todo -> mettre 5 minutes (300 secondes)
        
        # Speaker.setEngine(GttsEngine())
        
        
        # Constants
        # ---------------------------------------------------------------------------- #
        self.audio_dir = "./assets/audio/"
        
        
        from src.objects.displayer.Displayer import Displayer
        self.webApp = Displayer(self.test_mode).get_display()
        
        # Buttons PIN
        self.buttons_pins = [16, 14, 26, 17]
        self.button_wheel = 5
        self.button_start = 23
        
        
        self.hotspot_ip = "10.42.0.1"
        
    def stop_program(self):
        object = [
        {
            "type": "text",
            "content": "❌ Programme stoppé",
            "images": [],
            "style": ["text-big", "text-bold", "text-red", "text-centered"]
        }]
        # self.webApp.show(object)
        Debug.LogError("[Error]> Programme interrompu par l'utilisateur")
        self.webApp.exit()
        
@singleton
class ScoreConfig:
    def __init__(self):
        self.nb_question = 0
        self.nb_actual_question = 0
        self.total_score = 0
        self.quizzes_score = {"BlindTest" : [0,0], "CultureG": [0,0], "DevineSuite": [0, 0], "OuCest": [0, 0], "QuiSuisJe": [0, 0], "TroisImages": [0, 0]}
        
        self.numbers_question = [2, 7, 10, 12] # [5, 7, 10, 12]
    
    def update_nb_actual_question(self):
        Debug.LogPopup("+1 à la question !")
        self.nb_actual_question += 1
        
    def update_score(self, quiz, answer):
        if answer:
            self.total_score += 1
            self.quizzes_score[quiz][0] += 1
            self.quizzes_score[quiz][1] += 1
        else:
            self.quizzes_score[quiz][1] += 1
            