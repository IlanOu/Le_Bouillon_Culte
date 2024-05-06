# ----------------------------------- Main ----------------------------------- #

# from src.Application import App

# if __name__ == "__main__":
#     app = App()
#     app.run()


# -------------------------------- à supprimer ------------------------------- #


from src.quiz.QuizManager import QuizManager
from src.objects.rfid.RFIDReader import RFIDReader


# Exemple d'utilisation
rfid_reader = RFIDReader()
manager = QuizManager(rfid_reader)
manager.setup()
manager.run()



# ----------------------------------- Test ----------------------------------- #
""" 
from src.toolbox.Speaker import *

Speaker.say("Salut, je suis un texte de test ! Je parles parfaitement bien !", ElevenLabsEngine()) 
"""
