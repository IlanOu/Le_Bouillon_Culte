from src.quiz.quizzes.BlindTest import Quiz_BlindTest
from src.quiz.quizzes.DevineSuite import Quiz_DevineSuite
from src.quiz.quizzes.OuCest import Quiz_OuCest
from src.quiz.quizzes.QuiSuisJe import Quiz_QuiSuisJe
from src.quiz.quizzes.CultureG import Quiz_CultureG
from src.quiz.quizzes.TroisImages import Quiz_TroisImages

from src.quiz.Quiz import Quiz

from src.toolbox.Speaker import *
from src.toolbox.Debug import *
from src.toolbox.Standby import StandBy

from src.quiz.MusicPlayer import MusicPlayer

from src.objects.displayer.RollDisplayer import RollingNumberDisplay
from src.objects.button.Button import Button

from src.Config import Config, ScoreConfig

import random
import time
import threading


# ------------------------------- Quiz manager ------------------------------- #


class QuizManager:
    def __init__(self, sensors_manager):
        self.quizzes = []
        self.demo_quizzes = []
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
        
    def add_demo_quiz(self, quiz: Quiz):
        self.demo_quizzes.append(quiz)
    
    def remove_demo_quiz(self, quiz: Quiz):
        if len(self.demo_quizzes) > 0:
            self.demo_quizzes.remove(quiz)
        else:
            Debug.LogError("Il n'y a plus de quiz disponnible")
    
    def __get_random_quiz(self):
        random_quiz = random.choice(self.demo_quizzes)
        return random_quiz

    def __display_random_quiz(self):
        quizzes_names = []
        for quiz in self.quizzes:
            quizzes_names.append(quiz.name)
        
        random_quiz = self.__get_random_quiz()
        target_quiz = random_quiz.name
        num_rolls = 15

        
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
        for zone in ScoreConfig().quizzes_score:
            for scores in zone:
                scores = 0

        ScoreConfig().total_score = 0
        ScoreConfig().nb_actual_question = 0

        #? ---------------------------------------------------------------------------- #
        #?                                    1B - 3                                    #
        #? ---------------------------------------------------------------------------- #
        object = [
        {
            "type": "text",
            "content": "La partie va commencer !",
            "style": ["text-big", "text-uppercase", "text-blue", "text-centered"]
        }]
        Config().webApp.show(object)


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
        self.add_quiz(self.quiz1) # screens done (normalement)
        self.add_quiz(self.quiz2)
        self.add_quiz(self.quiz3) # screens done (normalement)
        self.add_quiz(self.quiz4) # screens done (normalement)
        self.add_quiz(self.quiz5) # screens done (normalement)
        self.add_quiz(self.quiz6) # screens done (normalement)
        
        # Add quizzes for demo
        self.add_demo_quiz(self.quiz1) # quiz3
        self.add_demo_quiz(self.quiz5)
        self.add_demo_quiz(self.quiz6)
        
        self.config_nb_question()
        
    def config_nb_question(self):
        question_value = "Combien de manches \nsouhaitez-vous jouer ?"
        

        #? ---------------------------------------------------------------------------- #
        #?                                    1B - 1                                    #
        #? ---------------------------------------------------------------------------- #
        items_questions = []
        
        demo_items_buttons_fake = [3, 5, 7, 10]
        
        for item in demo_items_buttons_fake:
            items_questions.append(str(item) + " questions")
        
        object = [{
                "type": "text",
                "content": question_value,
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
            },{
                "type": "table",
                "items": items_questions,
                "style": []
            },{
                "type": "text",
                "content": "Utilisez les boutons pour choisir",
                "style": ["text-medium", "text-italic", "text-black"]
            }]
        
        # Afficher et dire la question
        Config().webApp.show(object)
        Speaker.say(question_value.replace("/n", ""))
        
        # ---------------------------------------------------------------------------- #
        
        # Dire les réponses possibles
        str_choices = " questions ? ".join(map(str, demo_items_buttons_fake)) + " questions ?"
        Speaker.say(str_choices)
        
        
        # Afficher la réponse de l'utilisateur
        # ---------------------------------------------------------------------------- #

        
        
        #? ---------------------------------------------------------------------------- #
        #?                                    1B - 2                                    #
        #? ---------------------------------------------------------------------------- #
        
        button_pin = self.sensors_manager.wait_for_button_press()
        MusicPlayer(Config().audio_dir).play_threading("sounds/selected-answer.mp3")
        
        if not button_pin in Config().buttons_pins:
            Debug.LogError("Il n'y a pas autant de bouton que de cases dans le tableau ! Il en faut 4 !")
        
        index_answer = Config().buttons_pins.index(button_pin)
        
        answer_value = items_questions[index_answer]
        
        object = [{
                "type": "text",
                "content": question_value,
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
            },{
                "type": "table",
                "items": items_questions,
                "style": [],
                "answer": answer_value
            },{
                "type": "text",
                "content": "I",
                "style": ["text-medium", "text-white"]
            }]
        Config().webApp.show(object)
        
        time.sleep(1)
        
        ScoreConfig().nb_question = ScoreConfig().numbers_question[Config().buttons_pins.index(button_pin)]


        #? ---------------------------------------------------------------------------- #
        #?                                    1B - 3                                    #
        #? ---------------------------------------------------------------------------- #
        object = [{
                "type": "image",
                "content": "",
                "images": ["logos/Logo_image.webp"],
                "style": ["image-small"]
            },{
                "type": "text",
                "content": "La partie va \nbientôt commencer",
                "style": ["text-big", "text-uppercase", "text-bold-700", "text-blue", "text-centered"]
            }]
        
        Config().webApp.show(object)
        
        time.sleep(3)

    def read_rfid_worker(self):
        while True:
            if self.rfid_event.is_set():
                if self.sensors_manager.read_rfid():
                    self.rfid_response = Config().internal_RFID_zone
                    self.stop_rfid()
                    break
                self.rfid_event.clear()

    def wait_for_rfids(self):
        Debug.LogColor("[Action]> Passez le badge devant le capteur RFID...", Style.PURPLE + Style.ITALIC)
        
        self.rfid_response = None
        self.rfid_event.set()
        self.start_rfid()

        while self.rfid_response is None:
            time.sleep(0.1)

        self.set_zone(self.rfid_response)
        
        StandBy().reset()

    def run(self):
        ScoreConfig().update_nb_actual_question()
        
        # Wait for user press button
        # ---------------------------------------------------------------------------- #
        
        time.sleep(1)
        
        #? ---------------------------------------------------------------------------- #
        #?                                      2                                       #
        #? ---------------------------------------------------------------------------- #
        text_to_display = "Appuyez sur le bouton Rouge \npour commencer"
        
        object = [{
                "type": "text",
                "content": text_to_display,
                "style": ["text-big", "text-uppercase", "text-bold-700", "text-blue", "text-centered"]
            },{
                "type": "image",
                "content": "",
                "images": ["icons/big_button.webp"],
                "style": ["image-small"]
            }]
        Config().webApp.show(object)
        
        
        # looping = True
        
        # Repeat every 20s to press on the button
        # ---------------------------------------------------------------------------- #
        # def speek_text():
        #     while looping:
        #         Speaker.say(text_to_display)
        #         time.sleep(20)

        # thread = threading.Thread(target=speek_text)
        # thread.start()
        
        Speaker.say(text_to_display)
        
        self.sensors_manager.wait_for_button_press(Button(Config().button_wheel))
        MusicPlayer(Config().audio_dir).play_threading("sounds/selected-answer.mp3")
        
        
        looping = False
        
        
        #? ---------------------------------------------------------------------------- #
        #?                                  3B - 1                                      #
        #? ---------------------------------------------------------------------------- #
        
        time.sleep(1)
        
        # Display current question
        # ---------------------------------------------------------------------------- #
        to_display = f"Vous en êtes à la question {str(ScoreConfig().nb_actual_question)} sur {str(ScoreConfig().nb_question)}."
        object = [{
                "type": "text",
                "content": "Question",
                "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
            },{
                "type": "text",
                "content": str(ScoreConfig().nb_actual_question) + " / " + str(ScoreConfig().nb_question),
                "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered", "text-boxed-red"]
            }]
        
        
        if ScoreConfig().nb_actual_question == ScoreConfig().nb_question:
            to_display = "Attention, vous en êtes à la dernière question !"
            
            #? ---------------------------------------------------------------------------- #
            #?                                  3B - 2                                      #
            #? ---------------------------------------------------------------------------- #
            
            object = [{
                "type": "text",
                "content": "Dernière question",
                "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                }]
        
        
        Config().webApp.show(object)
        
        Speaker.say(to_display)
        
        
        # Turn the wheel
        # ---------------------------------------------------------------------------- #
        random_quiz = self.__display_random_quiz()
        self.__set_current_quiz(random_quiz)
        
        
        # Run quiz
        # ---------------------------------------------------------------------------- #
        try:
            if self.current_quiz != self.quiz2:
                
                if Config().game_first_lap:
                    #? ---------------------------------------------------------------------------- #
                    #?                                  4B - 1                                      #
                    #? ---------------------------------------------------------------------------- #
                    to_display = "Les questions sont posées \nen fonction de la région \nque vous choisissez."
                    object = [{
                            "type": "text",
                            "content": to_display,
                            "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                        }]
                    Config().webApp.show(object)
                    
                    Speaker.say(to_display)
                    
                    time.sleep(3)
                    
                    
                    #? ---------------------------------------------------------------------------- #
                    #?                                  4B - 2                                      #
                    #? ---------------------------------------------------------------------------- #
                    to_display = "Pour choisir une région, \nplacez votre pion sur \nune des régions de \ncouleur rouge."
                    object = [{
                            "type": "text",
                            "content": to_display,
                            "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                        }]
                    Config().webApp.show(object)
                    
                    Speaker.say(to_display)
                
                else:
                    #? ---------------------------------------------------------------------------- #
                    #?                                  4B - 2                                      #
                    #? ---------------------------------------------------------------------------- #
                    to_display = "Pour choisir une région, \nplacez votre pion sur \nune des régions de \ncouleur rouge"
                    object = [{
                            "type": "text",
                            "content": to_display,
                            "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                        }]
                    Config().webApp.show(object)
                    
                    Speaker.say(to_display)
                
                # Wait for RFID
                self.wait_for_rfids()
                
                MusicPlayer(Config().audio_dir).play_threading("sounds/pion-on-card.mp3")

                #? ---------------------------------------------------------------------------- #
                #?                                  4A - 2                                      #
                #? ---------------------------------------------------------------------------- #
                object = [{
                        "type": "text",
                        "content": "Vous avez choisi",
                        "style": ["text-medium", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                    },{
                        "type": "text",
                        "content": Config().zone,
                        "style": ["text-big", "text-uppercase", "text-bold-700", "text-blue", "text-centered"]
                    }]
                Config().webApp.show(object)
                
                time.sleep(1)
                
                Speaker.say("Vous avez choisi la région : " + Config().zone)
                
                time.sleep(3) 
                
            else:
                
                #? ---------------------------------------------------------------------------- #
                #?                                 Bonus 1                                      #
                #? ---------------------------------------------------------------------------- #
                to_display = "Attention !\nce jeu est différent des autres"
                
                object = [{
                        "type": "text",
                        "content": to_display,
                        "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                    }]
                
                
                Speaker.say(to_display)
                Config().webApp.show(to_display)

                time.sleep(3)
                
                
                #? ---------------------------------------------------------------------------- #
                #?                                 Bonus 2                                      #
                #? ---------------------------------------------------------------------------- #
                
                to_display = "Vous devrez placer le pion \naprès la question !"
                
                object = [{
                        "type": "text",
                        "content": to_display,
                        "style": ["text-big", "text-uppercase", "text-bold-700", "text-red", "text-centered"]
                    }]
                
                Config().webApp.show(to_display)
                Speaker.say(to_display)

                time.sleep(3)


            # Run quiz
            self.current_quiz.process()
            
            
            object = [{
                "type": "score",
                "question": "Question " + str(ScoreConfig().nb_actual_question) + "/" + str(ScoreConfig().nb_question),
                "score": "Score : " + str(ScoreConfig().total_score) + "/" + str(ScoreConfig().nb_actual_question),
                "style": []
            },{
                "type": "text",
                "content": "Reprennez le pion",
                "style": ["text-big", "text-uppercase", "text-red", "text-bold-700", "text-centered"]
            }]
        
            Config().webApp.show(object)
            
            Speaker.say("Reprenez le pion")
            
            time.sleep(3)
            
            
            self.remove_demo_quiz(self.current_quiz)
            
            # On finish, cleanup GPIO
            self.sensors_manager.cleanup()
        
        # ------------------------------- Stop program ------------------------------- #
        except KeyboardInterrupt:
            Config().stop_program()
    
    def receive_message(self, message):
        Debug.LogWhisper(f"[Websocket]> Message reçu dans QuizManager : {message}")
        self.rfid_response = message
