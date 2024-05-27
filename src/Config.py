from src.toolbox.Singleton import singleton
from src.toolbox.Debug import Debug
from src.objects.displayer.WebDisplayer import WebApp
from src.objects.displayer.ConsoleDisplayer import DisplayManager
from src.objects.displayer.Displayer import Displayer


@singleton
class Config:
    def __init__(self):
        self.test_mode = True
        
        self.audio_dir = "./assets/audio/"
        self.webApp = Displayer(self.test_mode).get_display()
        self.zone = "Auvergne-Rhône-Alpes" # Todo -> temp value / à changer plus tard en récupérant via les étapes précédentes dans l'Enum
        
        self.buttons_pins = [16, 17, 26, 23]
        
        
        
    def stop_program(self):
        self.webApp.show("❌ Programme stoppé", "stop")
        Debug.LogError("[Error]> Programme interrompu par l'utilisateur")
        self.webApp.exit()