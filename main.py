# from src.Application import App

# if __name__ == "__main__":
#     app = App()
#     app.run()


# -------------------------------- à supprimer ------------------------------- #


from src.quiz.Quiz import *

# Exemple d'utilisation
manager = QuizManager()
quiz1 = Quiz("quiz1.json")
quiz2 = Quiz("quiz2.json")
manager.add_quiz(quiz1)
manager.add_quiz(quiz2)
manager.run()