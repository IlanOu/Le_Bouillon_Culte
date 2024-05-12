from src.quiz.QuizManager import QuizManager
from src.objects.rfid.RFIDReader import RFIDReader


class App:
    def __init__(self):
        self.running = True
    
    def run(self):
        rfid_reader = RFIDReader()
        manager = QuizManager(rfid_reader)
        manager.setup()
        
        while self.running:
            manager.run()