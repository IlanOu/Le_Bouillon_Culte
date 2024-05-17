from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager
from src.objects.Checker import Checker

class App:
    def __init__(self):
        self.running = True
    
    
    def run(self):
        
        Checker().check_sensors()
        
        sensors_manager = SensorsManager()
        manager = QuizManager(sensors_manager)
        manager.setup()
        
        while self.running:
            manager.run()