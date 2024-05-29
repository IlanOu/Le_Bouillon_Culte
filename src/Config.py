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
        
        # Speaker.setEngine(GttsEngine())
        
        
        # Constants
        # ---------------------------------------------------------------------------- #
        self.audio_dir = "./assets/audio/"
        
        
        from src.objects.displayer.Displayer import Displayer
        self.webApp = Displayer(self.test_mode).get_display()
        
        
        self.buttons_pins = [16, 17, 26, 23]
        
        self.hotspot_ip = "10.42.0.1"
        
    def stop_program(self):
        self.webApp.show("❌ Programme stoppé", "stop")
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
        self.nb_actual_question += 1
        
    def update_score(self, quiz, answer):
        if answer:
            self.total_score += 1
            self.quizzes_score[quiz][0] += 1
            self.quizzes_score[quiz][1] += 1
        else:
            self.quizzes_score[quiz][1] += 1
            