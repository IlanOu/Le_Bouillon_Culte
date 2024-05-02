import random

class Quiz:
    def __init__(self):
        self.questions = [
            "Pourquoi les nuages sont blancs ?",
            "Combien de grains de sable y a-t-il dans le désert ?",
            "Est-ce que les poissons rouges peuvent nager à l'envers ?",
            "Pourquoi le ciel est bleu ?",
            "Est-ce que les chats peuvent voir dans le noir ?",
            "Combien de temps faut-il pour cuire un œuf sur le trottoir en plein soleil ?",
            "Est-ce que les pingouins ont des genoux ?",
            "Pourquoi les arbres sont verts ?",
            "Est-ce que les chiens peuvent regarder la télévision ?",
            "Combien de temps faut-il pour que la lumière du soleil atteigne la Terre ?",
            "Est-ce que les éléphants ont peur des souris ?",
            "Pourquoi les girafes ont un long cou ?",
            "Est-ce que les canards peuvent voler à reculons ?",
            "Combien de grains de riz peut-on mettre dans un verre ?",
            "Est-ce que les escargots laissent des traces de bave sur les vitres ?",
            "Pourquoi les abeilles font-elles du miel ?",
            "Est-ce que les papillons peuvent compter jusqu'à dix ?",
            "Combien de temps faut-il pour qu'un arbre pousse d'un mètre ?",
            "Est-ce que les grenouilles peuvent respirer sous l'eau ?",
            "Pourquoi les bananes sont-elles courbées ?"
        ]
        
        self.responses = [
            "C'est faux !",
            "Mauvaise réponse !",
            "C'est une mauvaise réponse pour vous !",
            "C'est encore une mauvaise réponse...",
            "Décidément, vous n'êtes vraiment pas doués",
            "C'est toujours faux. Vous le faites exprès ? C'est pourtant facile."
        ]

    def get_random_question(self):
        return random.choice(self.questions)
    
    def get_random_response(self):
            return random.choice(self.responses)