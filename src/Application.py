from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager
from src.objects.Checker import Checker
from src.toolbox.Websocket import WebSocketServerThread
from src.Config import ScoreConfig

from src.toolbox.Debug import Debug
from src.toolbox.Standby import StandBy

from src.Config import Config

from src.quiz.MusicPlayer import MusicPlayer


import time

class App:
    def __init__(self):
        self.running = True
        self.server_thread = None
        
        self.start_app()
        
    def start_app(self):
        
        #? ---------------------------------------------------------------------------- #
        #?                                    Start                                     #
        #? ---------------------------------------------------------------------------- #
        object = [
        {
            "type": "text",
            "content": "I",
            "style": ["text-white"]
        }]
        Config().webApp.show(object)
        
        time.sleep(5)
        
        #? ---------------------------------------------------------------------------- #
        #?                                    1A - 1                                    #
        #? ---------------------------------------------------------------------------- #
        object = [
        {
            "type": "image",
            "content": "",
            "images": ["logos/Logo_full.webp"],
            "style": ["image-medium"]
        }]
        Config().webApp.show(object)
        
        MusicPlayer(Config().audio_dir).play_threading("sounds/0.mp3")
         
        time.sleep(5)
        
        
        #? ---------------------------------------------------------------------------- #
        #?                                    1A - 2                                    #
        #? ---------------------------------------------------------------------------- #
        object = [
        {
            "type": "text",
            "content": "Bonjour !\nEt bienvenue dans",
            "images": [],
            "style": ["text-medium", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
        },
        {
            "type": "image",
            "content": "",
            "images": ["logos/Logo_text.webp"],
            "style": ["image-medium"]
        }]
        
        Config().webApp.show(object)
        
        MusicPlayer(Config().audio_dir).play_threading("sounds/1A.mp3")
        
        
        time.sleep(3)
        
        
        #? ---------------------------------------------------------------------------- #
        #?                                    1A - 3                                    #
        #? ---------------------------------------------------------------------------- #
        object = [
        {
            "type": "image",
            "content": "",
            "images": ["logos/Logo_image.webp"],
            "style": ["image-small"]
        },
        {
            "type": "text",
            "content": "Le jeu qui teste\nvos connaissances\net votre mémoire.",
            "style": ["text-big", "text-uppercase", "text-bold-700", "text-blue", "text-centered"]
        }]
        
        Config().webApp.show(object)
        
        time.sleep(5)

    def run(self):
        if Config().use_ESP_connection:
            host = "0.0.0.0"
            port = 8080
            self.server_thread = WebSocketServerThread(host, port)
            Debug.LogWhisper(f"[Websocket]> Serveur WebSocket démarré sur {host}:{port}")
            self.server_thread.start()
            if Config().checker_active:
                checker = Checker()
                checker.check_sensors(self.server_thread)
            else:
                self.server_thread.send_message_to_all("launch")

        sensors_manager = SensorsManager()
        manager = QuizManager(sensors_manager)
        StandBy(sensors_manager)
        
        while True:
            manager.setup(self.server_thread)
            
            for _ in range (ScoreConfig().nb_question):
                manager.run()

            object = [{
                "type": "image",
                "images": ["logos/Logo_full.webp"],
                "style": ["image-medium"]
            },{
                "type": "text",
                "content": "Fin de la partie",
                "style": ["text-big", "text-uppercase", "text-blue", "text-bold-700", "text-centered"]
            }]
        
            Config().webApp.show(object)
            
            time.sleep(5)
            
            
            object = [{
                    "type": "image",
                    "images": ["logos/Logo_full.webp"],
                    "style": ["image-medium"]
                },{
                    "type": "text",
                    "content": "Votre score est de",
                    "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                },{
                    "type": "text",
                    "content": str(ScoreConfig().total_score) + " / " + str(ScoreConfig().nb_question),
                    "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered", "text-boxed-red"]
                }]
            
            Config().webApp.show(object)
            
            time.sleep(10)
            
            

    def receive_message(self, message):
        Debug.LogWhisper(f"[Websocket]> Message reçu dans App : {message}")
