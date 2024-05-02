from src.toolbox.Speeker import Speaker, GttsEngine, Pyttsx3Engine
from src.objects.Displayer.WebDisplayer import WebApp, StringUpdater
import threading
from src.toolbox.Debug import Debug, Style
import time
from src.quiz.Quiz import Quiz
from src.objects.rfid.RFIDReader import RFIDReader



class App:
    def __init__(self):
        self.quiz = Quiz()
        self.rfid_reader = RFIDReader()
        self.string_updater = StringUpdater(update_interval=1)
        self.web_app = WebApp(self.string_updater)

    def run(self):
        thread_rfid = threading.Thread(target=self.rfid_thread)
        thread_rfid.start()
        self.web_app.run()
        thread_rfid.join()

    def rfid_thread(self):
        try:
            while True:
                id, text = self.rfid_reader.read_rfid()
                
                # Questions
                # ---------------------------------------------------------------------------- #
                question = self.quiz.get_random_question()
                Debug.LogColor(f"Question : {question}", [Style.OK_CYAN, Style.UNDERLINE])
                Speaker.say(question, GttsEngine())
                self.string_updater.write(question=question, answer="")
                
                self.rfid_reader.wait_for_button_press()
                
                
                # Responses
                # ---------------------------------------------------------------------------- #
                response = self.quiz.get_random_response()
                Debug.LogColor(f"Réponse : {response}", [Style.PURPLE, Style.ITALIC])
                Speaker.say(response, GttsEngine())
                self.string_updater.write(question=question, answer=response)
                
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            Debug.LogSuccess("Programme interrompu par l'utilisateur")
        finally:
            self.rfid_reader.cleanup()

