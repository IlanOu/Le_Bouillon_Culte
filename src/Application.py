from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager
from src.objects.Checker import Checker
from src.toolbox.Websocket import WebSocketServerThread
from src.Config import ScoreConfig

from src.toolbox.Debug import Debug

from src.Config import Config

import time

class App:
    def __init__(self):
        self.running = True
        self.server_thread = None
        
        self.start_app()
        
    def start_app(self):
        
        object = [
        {
            "type": "image",
            "content": "",
            "images": ["Logo_full.jpg"],
            "style": ["image-big"]
        }]
        
        Config().webApp.show(object)
        time.sleep(1)
        
        
        object = [
        {
            "type": "text",
            "content": "Bonjour !\nEt bienvenue dans",
            "images": [],
            "style": ["text-big", "text-bold", "text-red", "text-centered"]
        },
        {
            "type": "image",
            "content": "",
            "images": ["Logo_text.jpg"],
            "style": ["image-big"]
        }]
        
        Config().webApp.show(object)
        time.sleep(1)
        
        
        object = [
        {
            "type": "image",
            "content": "",
            "images": ["Logo_image.jpg"],
            "style": ["image-big"]
        },
        {
           "type": "text",
            "content": "Le jeu qui teste\nvos connaissances\net votre mémoire.",
            "images": [],
            "style": ["text-big", "text-bold", "text-red", "text-centered"]
        }]
        
        Config().webApp.show(object)
        time.sleep(1)

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
        
        manager.setup(self.server_thread)
        
        for i in range (ScoreConfig().nb_question):
            manager.run()
            
        Config().stop_program()

    def receive_message(self, message):
        Debug.LogWhisper(f"[Websocket]> Message reçu dans App : {message}")
