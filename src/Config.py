from src.toolbox.Singleton import singleton
from src.toolbox.Debug import Debug
from src.objects.displayer.WebDisplayer import WebApp


@singleton
class Config:
    def __init__(self):
        self.audio_dir = "./assets/audio/"
        self.webApp = WebApp()
        self.zone = "Auvergne-Rhône-Alpes" # Todo -> temp value / à changer plus tard en récupérant via les étapes précédentes dans l'Enum
        
    def stopProgram(self):
        self.webApp.show("❌ Programme stoppé", "stop")
        Debug.LogError("[Error]> Programme interrompu par l'utilisateur")
        self.webApp.exit()