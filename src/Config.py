from src.toolbox.Singleton import singleton
from src.toolbox.Debug import Debug
from src.objects.displayer.WebDisplayer import WebApp


@singleton
class Config:
    def __init__(self):
        self.audio_dir = "./assets/audio/"
        self.webApp = WebApp()
        self.zone = "Auvergne-Rhône-Alpes"
        
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
    
    def update_nb_actual_question(self):
        self.nb_actual_question += 1
        
    def update_score(self, quiz, answer):
        if answer:
            self.total_score += 1
            self.quizzes_score[quiz][0] += 1
            self.quizzes_score[quiz][1] += 1
        else:
            self.quizzes_score[quiz][1] += 1
            