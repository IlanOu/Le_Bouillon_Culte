import json
import random
from src.toolbox.Debug import Debug

Debug.prefixActive = False

# Quiz protocol
# ---------------------------------------------------------------------------- #

class Quiz:
    def __init__(self, json_file=""):
        # self.json_file = json_file
        # self.questions = []
        # self.responses = []
        
        # if json_file != "":
        #     self.fill_questions()
        #     self.fill_responses()
        pass

    def fill_questions(self):
        # with open(self.json_file, 'r') as file:
        #     data = json.load(file)
        #     self.questions = data.get('question', [])
        pass

    def fill_responses(self):
        # with open(self.json_file, 'r') as file:
        #     data = json.load(file)
        #     self.responses = data.get('answers', [])
        pass

    def get_random_question(self):
        # raise NotImplementedError("La méthode get_random_question doit être implémentée dans les classes dérivées.")
        pass

    def get_random_response(self):
        # raise NotImplementedError("La méthode get_random_response doit être implémentée dans les classes dérivées.")
        pass


# Quizzes
# ---------------------------------------------------------------------------- #

class QuizA(Quiz):
    def get_random_question(self):
        # return random.choice(self.questions)
        pass

    def get_random_response(self):
        # return random.choice(self.responses)
        pass


class QuizB(Quiz):
    def get_random_question(self):
        # Implémentation spécifique pour QuizB
        pass

    def get_random_response(self):
        # Implémentation spécifique pour QuizB
        pass


class QuizC(Quiz):
    def get_random_question(self):
        # Implémentation spécifique pour QuizB
        pass

    def get_random_response(self):
        # Implémentation spécifique pour QuizB
        pass


class QuizD(Quiz):
    def get_random_question(self):
        # Implémentation spécifique pour QuizB
        pass

    def get_random_response(self):
        # Implémentation spécifique pour QuizB
        pass


class QuizE(Quiz):
    def get_random_question(self):
        # Implémentation spécifique pour QuizB
        pass

    def get_random_response(self):
        # Implémentation spécifique pour QuizB
        pass


class QuizF(Quiz):
    def get_random_question(self):
        # Implémentation spécifique pour QuizB
        pass

    def get_random_response(self):
        # Implémentation spécifique pour QuizB
        pass


# Quiz manager
# ---------------------------------------------------------------------------- #

class QuizManager:
    def __init__(self):
        self.quizzes = []
        self.current_quiz = None
        self.state = 'start'

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def start(self):
        self.state = 'choose_quiz'

    def choose_quiz(self):
        if len(self.quizzes) == 0:
            Debug.Log("Aucun quiz disponible.")
            self.state = 'end'
        else:
            Debug.Log("Choisis un quiz :")
            for i, quiz in enumerate(self.quizzes):
                Debug.Log(f"{i + 1}. {quiz.json_file}")
            choice = int(input("Entrez le numéro du quiz : "))
            self.current_quiz = self.quizzes[choice - 1]
            self.state = 'run_quiz'

    def run_quiz(self):
        question = self.current_quiz.get_random_question()
        Debug.Log(question)
        response = input("Votre réponse : ")
        correct_response = self.current_quiz.get_random_response()
        if response.lower() == correct_response.lower():
            Debug.Log("Bravo, c'est la bonne réponse !")
        else:
            Debug.Log(f"Désolé, la réponse attendue était '{correct_response}'.")
        self.state = 'choose_quiz'

    def run(self):
        while self.state != 'end':
            if self.state == 'start':
                self.start()
            elif self.state == 'choose_quiz':
                self.choose_quiz()
            elif self.state == 'run_quiz':
                self.run_quiz()



# # Exemple d'utilisation
# ---------------------------------------------------------------------------- #
# manager = QuizManager()
# quiz1 = QuizA("quiz1.json")
# quiz2 = QuizB("quiz2.json")
# # Ajoutez les autres instances de quiz
# manager.add_quiz(quiz1)
# manager.add_quiz(quiz2)
# manager.run()