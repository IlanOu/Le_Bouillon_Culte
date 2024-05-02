import json
import random

class Quiz:
    def __init__(self, json_file=""):
        self.json_file = json_file
        self.questions = ["Salut, comment vons-je ?", "Je suis un lapin ?"]
        self.responses = ["Eu, okay", "Non merci"]
        
        if (json_file != ""):
            self.fill_questions()
            self.fill_responses()

    def fill_questions(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            self.questions = data.get('question', [])

    def fill_responses(self):
        with open(self.json_file, 'r') as file:
            data = json.load(file)
            self.responses = data.get('answers', [])

    def get_random_question(self):
        return random.choice(self.questions)

    def get_random_response(self):
        return random.choice(self.responses)

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
            print("Aucun quiz disponible.")
            self.state = 'end'
        else:
            print("Choisis un quiz :")
            for i, quiz in enumerate(self.quizzes):
                print(f"{i + 1}. {quiz.json_file}")
            choice = int(input("Entrez le numéro du quiz : "))
            self.current_quiz = self.quizzes[choice - 1]
            self.state = 'run_quiz'

    def run_quiz(self):
        question = self.current_quiz.get_random_question()
        print(question)
        response = input("Votre réponse : ")
        correct_response = self.current_quiz.get_random_response()
        if response.lower() == correct_response.lower():
            print("Bravo, c'est la bonne réponse !")
        else:
            print(f"Désolé, la réponse attendue était '{correct_response}'.")
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
# manager = QuizManager()
# quiz1 = Quiz("quiz1.json")
# quiz2 = Quiz("quiz2.json")
# manager.add_quiz(quiz1)
# manager.add_quiz(quiz2)
# manager.run()