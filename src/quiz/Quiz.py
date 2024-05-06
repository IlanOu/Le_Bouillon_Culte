from src.toolbox.Debug import Debug

Debug.prefixActive = False


# ------------------------------- Quiz protocol ------------------------------ #

class Quiz:
    def __init__(self, rfid_reader, jsonpath=""):
        self.name=""
        self.jsonpath = jsonpath
        self.datas = {}
        self.rfid_reader = rfid_reader

    def process(self):
        Debug.LogError("La méthode get_random_question doit être implémentée dans les classes dérivées.")

