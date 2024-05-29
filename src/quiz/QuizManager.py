from src.quiz.quizzes.BlindTest import Quiz_BlindTest
from src.quiz.quizzes.DevineSuite import Quiz_DevineSuite
from src.quiz.quizzes.OuCest import Quiz_OuCest
from src.quiz.quizzes.QuiSuisJe import Quiz_QuiSuisJe
from src.quiz.quizzes.CultureG import Quiz_CultureG
from src.quiz.quizzes.TroisImages import Quiz_TroisImages

from src.quiz.Quiz import Quiz

from src.toolbox.Speaker import *

from src.objects.displayer.RollDisplayer import RollingNumberDisplay

from src.toolbox.Debug import *

from src.Config import Config, ScoreConfig


import random
import time
import threading



# ------------------------------- Quiz manager ------------------------------- #


class QuizManager:
    def __init__(self, sensors_manager):
        self.quizzes = []
        self.current_quiz = None
        
        self.sensors_manager = sensors_manager
        
        self.rfid_response = None
        self.rfid_thread = None
        self.rfid_event = threading.Event()
        self.rfid_is_started = False

    def set_zone(self, zone):
        Config().zone = zone

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

    def start_rfid(self):
        if not self.rfid_is_started:
            self.rfid_thread = threading.Thread(target=self.read_rfid_worker)
            self.rfid_thread.start()
            self.rfid_is_started = True
    
    def stop_rfid(self):
        if self.rfid_is_started:
            self.rfid_event.set()
            self.rfid_is_started = False
    
    def setup(self, server_thread=None):

        if server_thread != None:
            server_thread.addCallbackRun(self.receive_message)
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
        #self.add_quiz(self.quiz3) # Fait
        # self.add_quiz(self.quiz4) # Fait
        # self.add_quiz(self.quiz5) # Fait
        self.add_quiz(self.quiz6) # Fait
        
        self.config_nb_question()
        
    def config_nb_question(self):
        
        question_value = "Combien de question voulez-vous faire ?"
        
        # System
        # ---------------------------------------------------------------------------- #
        
        # 1. Display question
        Config().webApp.show(question_value, "text")
        Speaker.say(question_value.replace("/n", ""))
        
        # 2.
        table = "|".join(map(str, ScoreConfig().numbers_question))
        Config().webApp.show(table, "table")
        
        str_choices = ", ".join(map(str, ScoreConfig().numbers_question))
        
        Speaker.say(str_choices)
    
        # 3. Wait for response
        button_pin = self.sensors_manager.wait_for_button_press()
        
        
        if not button_pin in Config().buttons_pins:
            Debug.LogError("Il n'y a pas autant de bouton que de cases dans le tableau ! Il en faut 4 !")

        ScoreConfig().nb_question = ScoreConfig().numbers_question[Config().buttons_pins.index(button_pin)]

    def read_rfid_worker(self):
        while True:
            if self.rfid_event.is_set():
                if self.sensors_manager.read_rfid():
                    self.rfid_response = "Bretagne"
                    self.stop_rfid()
                    break
                self.rfid_event.clear()

    def wait_for_rfids(self):
        Debug.LogColor("[Action]> Passez le badge devant le capteur RFID...", Style.PURPLE + Style.ITALIC)
        Config().webApp.show("Placez le pion sur la carte")
        
        self.rfid_response = None
        self.rfid_event.set()
        self.start_rfid()

        while self.rfid_response is None:
            time.sleep(0.1)

        self.set_zone(self.rfid_response)


    def run(self):
        ScoreConfig().update_nb_actual_question()
        
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
                self.wait_for_rfids()

            # Run quiz
            self.current_quiz.process()
            
            # On finish, cleanup GPIO
            self.sensors_manager.cleanup()
        
        # ------------------------------- Stop program ------------------------------- #
        except KeyboardInterrupt:
            Config().webApp.show("❌ Programme stoppé", "stop")
            Debug.LogError("[Error]> Programme interrompu par l'utilisateur")
    
    def receive_message(self, message):
        Debug.LogWhisper(f"[Websocket]> Message reçu dans QuizManager : {message}")
        self.rfid_response = message
