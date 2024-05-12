from src.toolbox.Debug import Debug

Debug.prefixActive = False


# ------------------------------- Quiz protocol ------------------------------ #

class Quiz:
    def __init__(self, sensors_manager, jsonpath=""):
        self.name=""
        self.jsonpath = jsonpath
        self.datas = {}
        self.sensors_manager = sensors_manager

    def process(self):
        Debug.LogError("La méthode get_random_question doit être implémentée dans les classes dérivées.")

