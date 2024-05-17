# ----------------------------------- Main ----------------------------------- #

from src.Application import App
from src.Config import Config

if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        Config().stop_program()


# ----------------------------------- Test ----------------------------------- #
""" 
from src.toolbox.Speaker import *

Speaker.say("Salut, je suis un texte de test ! Je parles parfaitement bien !", ElevenLabsEngine()) 
"""
