from src.toolbox.Singleton import singleton
from src.toolbox.Debug import Debug
from src.objects.displayer.WebDisplayer import WebApp

@singleton
class Config:
    def __init__(self):
        self.audio_dir = "./assets/audio/"
        self.webApp = WebApp()
        
    def stopProgram(self):
        self.webApp.show("❌ Programme stoppé", "stop")
        Debug.LogError("[Error]> Programme interrompu par l'utilisateur")