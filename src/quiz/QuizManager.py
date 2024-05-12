from src.quiz.quizzes.BlindTest import Quiz_BlindTest
from src.quiz.quizzes.DevineSuite import Quiz_DevineSuite
from src.quiz.quizzes.OuCest import Quiz_OuCest
from src.quiz.quizzes.QuiSuisJe import Quiz_QuiSuisJe
from src.quiz.quizzes.CultureG import Quiz_CultureG
from src.quiz.quizzes.TroisImages import QuizF

from src.quiz.Quiz import Quiz

from src.objects.Displayer.RollDisplayer import RollingNumberDisplay


from src.toolbox.Debug import Debug

import random
import time

Debug.prefixActive = False

# ------------------------------- Quiz manager ------------------------------- #


class QuizManager:
    def __init__(self, rfid_reader):
        self.quizzes = []
        self.current_quiz = None
        self.zone = ""
        self.rfid_reader = rfid_reader

    def set_zone(self, zone):
        self.zone = zone

    def add_quiz(self, quiz: Quiz):
        self.quizzes.append(quiz)
        
    def __get_random_quiz(self):
        random_quiz = random.choice(self.quizzes)
        return random_quiz

    
    def __display_random_quiz(self):
        quizzes_names = []
        for quiz in self.quizzes:
            quizzes_names.append(quiz.name)
        
        random_quiz = self.__get_random_quiz()
        target_quiz = random_quiz.name
        num_rolls = 20

        rolling_display = RollingNumberDisplay(quizzes_names, target_quiz, num_rolls)
        rolling_display.display_rolling_number()
        
        time.sleep(3)
        
        return random_quiz 


    def __set_current_quiz(self, quiz: Quiz):
        self.current_quiz = quiz

    
    def setup(self):
        quiz1 = Quiz_BlindTest(self.rfid_reader, "./assets/json/blind_test.json")
        # quiz2 = Quiz_OuCest(self.rfid_reader, "./assets/json/ou_cest.json")
        # quiz3 = Quiz_DevineSuite(self.rfid_reader, "./assets/json/devine_suite.json")
        quiz4 = Quiz_QuiSuisJe(self.rfid_reader, "./assets/json/qui_suis_je.json")
        quiz5 = Quiz_CultureG(self.rfid_reader, "./assets/json/culture_g.json")
        # quiz6 = Quiz_(self.rfid_reader, "./assets/json/.json")

        self.add_quiz(quiz1) # à mettre avant le 13/05
        # self.add_quiz(quiz2) # Todo -> à faire
        # self.add_quiz(quiz3) # Todo -> à faire

        self.add_quiz(quiz4) # à mettre avant le 13/05
        self.add_quiz(quiz5) # à mettre avant le 13/05

        # self.add_quiz(quiz6)

        # self.__set_current_quiz(quiz1)

    def run(self):
        self.rfid_reader.webApp.show("Faites tourner la roue !")
        Debug.LogSeparator("Appuyez sur 'Entré' pour lancer")
        input("")
        random_quiz = self.__display_random_quiz()
        self.__set_current_quiz(random_quiz)
        
        
        if self.current_quiz == None:
            Debug.LogError("Définissez d'abord le quiz ! [ Utilisez setup() ]")
        try:
            self.rfid_reader.read_rfid()
            
            self.current_quiz.process()
        except KeyboardInterrupt:
            self.rfid_reader.webApp.show("❌ Programme stoppé", "stop")
            Debug.LogError("Programme interrompu par l'utilisateur")
