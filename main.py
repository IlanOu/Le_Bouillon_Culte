# from src.Application import App

# if __name__ == "__main__":
#     app = App()
#     app.run()


# -------------------------------- à supprimer ------------------------------- #

from src.quiz.Quiz import *

# Exemple d'utilisation
manager = QuizManager()

quiz1 = Quiz_BlindTest("./assets/blind_test.json")
quiz2 = Quiz_OuCest("./assets/ou_cest.json")
quiz3 = Quiz_DevineSuite("./assets/devine_suite.json")
quiz4 = Quiz_QuiSuisJe("./assets/qui_suis_je.json")
quiz5 = Quiz_CultureG("./assets/culture_g.json")
# quiz6 = Quiz_("./assets/.json")

manager.add_quiz(quiz1)
# manager.add_quiz(quiz2)

manager.set_current_quiz(quiz1)
manager.run()


 
# ----------------------------------- Test ----------------------------------- #
""" 
from src.toolbox.Speeker import *

Speaker.say("Salut, je suis un texte de teste ! Je parles parfaitement bien !", ElevenLabsEngine()) """