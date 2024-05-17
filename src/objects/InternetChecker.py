import socket
from src.toolbox.Debug import Debug, Style
from src.Config import Config

class InternetChecker:
    def __init__(self):
        self.host = "8.8.8.8"
        self.port = 53
        self.timeout = 3


    def is_connected(self):
        try:
            socket.setdefaulttimeout(self.timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
            return True
        except socket.error as ex:
            print(ex)
            return False


    def check_internet_connection(self):
        Debug.LogColor("[Check]> Check internet connection", Style.PURPLE + Style.ITALIC)
        
        if not self.is_connected():
            Config().webApp.show("Vous n'êtes pas connecté à internet", "stop")
            return {"pass": False, "message": "Vous n'êtes pas connecté à internet"}
        
        return {"pass": True, "message": ""}
        