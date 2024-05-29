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