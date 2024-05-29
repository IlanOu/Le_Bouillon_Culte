from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager
from src.objects.Checker import Checker
from src.toolbox.Websocket import WebSocketServerThread
from Config import ScoreConfig

from src.toolbox.Debug import Debug

from src.Config import Config

import time

class App:
    def __init__(self):
        self.running = True
        self.server_thread = None
        
        self.start_app()
        
    def start_app(self):
        Config().webApp.show("Bienvenue sur le Bouillon Culte !")
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
        manager.setup(self.server_thread)

        for i in range (ScoreConfig().nb_question):
            manager.run()

    def receive_message(self, message):
        Debug.LogWhisper(f"[Websocket]> Message reçu dans App : {message}")
