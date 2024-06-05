# ----------------------------------- Main ----------------------------------- #

from src.Application import App
from src.Config import Config

if __name__ == "__main__":
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        Config().stop_program()
