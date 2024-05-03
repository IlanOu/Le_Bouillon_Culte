# from src.Application import App

# if __name__ == "__main__":
#     app = App()
#     app.run()


# -------------------------------- à supprimer ------------------------------- #

from src.quiz.Quiz import *

# Exemple d'utilisation
manager = QuizManager()

quiz1 = Quiz_BlindTest("./assets/json/blind_test.json")
quiz2 = Quiz_OuCest("./assets/json/ou_cest.json")
quiz3 = Quiz_DevineSuite("./assets/json/devine_suite.json")
quiz4 = Quiz_QuiSuisJe("./assets/json/qui_suis_je.json")
quiz5 = Quiz_CultureG("./assets/json/culture_g.json")
# quiz6 = Quiz_("./assets/json/.json")

manager.add_quiz(quiz1)
# manager.add_quiz(quiz2) # Todo -> à faire
# manager.add_quiz(quiz3) # Todo -> à faire
# manager.add_quiz(quiz4)
# manager.add_quiz(quiz5)
# manager.add_quiz(quiz6)

# manager.set_current_quiz(quiz1)
random_quiz = manager.get_random_quiz()
manager.set_current_quiz(random_quiz)

manager.run()


 
# ----------------------------------- Test ----------------------------------- #
""" 
from src.toolbox.Speaker import *

Speaker.say("Salut, je suis un texte de teste ! Je parles parfaitement bien !", ElevenLabsEngine()) 
"""