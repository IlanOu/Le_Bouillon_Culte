from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager
from src.objects.Checker import Checker

from src.toolbox.Websocket import WebSocketServerThread

class App:
    def __init__(self):
        self.running = True
    
    
    def run(self):
        
        host = "0.0.0.0"
        port = 8080
        server_thread = WebSocketServerThread(host, port)
        print(f"Serveur WebSocket démarré sur {host}:{port}")
        server_thread.start()
        
        Checker().check_sensors()
        
        sensors_manager = SensorsManager()
        manager = QuizManager(sensors_manager)
        manager.setup()
        
        while self.running:
            manager.run()