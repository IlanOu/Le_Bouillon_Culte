from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager
from src.objects.Checker import Checker
from src.toolbox.Websocket import WebSocketServerThread

from src.toolbox.Debug import Debug

from src.Config import Config

class App:
    def __init__(self):
        self.running = True
        self.server_thread = None

    def run(self):
        if Config().use_ESP_connection:
            host = "0.0.0.0"
            port = 8080
            self.server_thread = WebSocketServerThread(host, port)
            Debug.LogWhisper(f"Serveur WebSocket démarré sur {host}:{port}")
            self.server_thread.start()
            if Config().checker_active:
                checker = Checker()
                checker.check_sensors(self.server_thread)
            else:
                self.server_thread.send_message_to_all("launch")

        sensors_manager = SensorsManager()
        manager = QuizManager(sensors_manager)
        manager.setup(self.server_thread)

        while self.running:
            manager.run()

    def receive_message(self, message):
        print(f"Message reçu dans App : {message}")
