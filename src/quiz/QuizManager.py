from src.quiz.quizzes.BlindTest import Quiz_BlindTest
from src.quiz.quizzes.DevineSuite import Quiz_DevineSuite
from src.quiz.quizzes.OuCest import Quiz_OuCest
from src.quiz.quizzes.QuiSuisJe import Quiz_QuiSuisJe
from src.quiz.quizzes.CultureG import Quiz_CultureG
from src.quiz.quizzes.TroisImages import Quiz_TroisImages

from src.quiz.Quiz import Quiz

from src.objects.displayer.RollDisplayer import RollingNumberDisplay

from src.toolbox.Debug import Debug, Style

from src.Config import Config


import random
import time


Debug.prefixActive = False

# ------------------------------- Quiz manager ------------------------------- #

class QuizManager:
    def __init__(self, sensors_manager):
        self.quizzes = []
        self.current_quiz = None
        self.zone = ""
        self.sensors_manager = sensors_manager

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
        
        # Get quizzes json content
        # ---------------------------------------------------------------------------- #
        self.quiz1 = Quiz_BlindTest(self.sensors_manager, "./assets/json/blind_test.json")
        self.quiz2 = Quiz_OuCest(self.sensors_manager, "./assets/json/ou_cest.json")
        self.quiz3 = Quiz_DevineSuite(self.sensors_manager, "./assets/json/devine_suite.json")
        self.quiz4 = Quiz_QuiSuisJe(self.sensors_manager, "./assets/json/qui_suis_je.json")
        self.quiz5 = Quiz_CultureG(self.sensors_manager, "./assets/json/culture_g.json")
        self.quiz6 = Quiz_TroisImages(self.sensors_manager, "./assets/json/3_images.json")


        # Add quizzes to the system
        # ---------------------------------------------------------------------------- #
        # self.add_quiz(self.quiz1) # Fait
        # self.add_quiz(self.quiz2) # Fait
        # self.add_quiz(self.quiz3) # Fait
        # self.add_quiz(self.quiz4) # Fait
        # self.add_quiz(self.quiz5) # Fait
        self.add_quiz(self.quiz6) # Fait


    def run(self):
        # Turn the wheel
        # ---------------------------------------------------------------------------- #
        Config().webApp.show("La partie va commencer !")
        Debug.LogColor("[Action]> Appuyez sur la touche 'Entrer ↵' pour lancer", Style.PURPLE + Style.ITALIC)
        input("")
        random_quiz = self.__display_random_quiz()
        self.__set_current_quiz(random_quiz)
        
        if self.current_quiz == None:
            Debug.LogError("[Error]> Aucun quiz n'est définit")
        
        # Run quiz
        # ---------------------------------------------------------------------------- #
        try:
            if self.current_quiz != self.quiz2:
                # Wait for RFID
                self.sensors_manager.read_rfid()
            
            # Run quiz
            self.current_quiz.process()
            
            # On finish, cleanup GPIO
            self.sensors_manager.cleanup()
        
        # ------------------------------- Stop program ------------------------------- #
        except KeyboardInterrupt:
            Config().webApp.show("❌ Programme stoppé", "stop")
            Debug.LogError("[Error]> Programme interrompu par l'utilisateur")
