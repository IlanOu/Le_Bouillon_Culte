from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager
from src.objects.Checker import Checker
from src.toolbox.Websocket import WebSocketServerThread

class App:
    def __init__(self):
        self.running = True
        self.server_thread = None

    def run(self):
        host = "0.0.0.0"
        port = 8080
        self.server_thread = WebSocketServerThread(host, port)
        print(f"Serveur WebSocket démarré sur {host}:{port}")
        self.server_thread.start()

        checker = Checker()
        checker.check_sensors(self.server_thread)

        sensors_manager = SensorsManager()
        manager = QuizManager(sensors_manager)
        manager.setup(self.server_thread)

        while self.running:
            manager.run()

    def receive_message(self, message):
        print(f"Message reçu dans App : {message}")
        # Vous pouvez traiter le message ici ou le transmettre à d'autres parties de votre application