from src.quiz.QuizManager import QuizManager
from src.objects.SensorsManager import SensorsManager


class App:
    def __init__(self):
        self.running = True
    
    
    def run(self):
        sensors_manager = SensorsManager()
        manager = QuizManager(sensors_manager)
        manager.setup()
        
        while self.running:
            manager.run()