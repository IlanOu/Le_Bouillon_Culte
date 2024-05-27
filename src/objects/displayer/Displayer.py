from src.objects.displayer.WebDisplayer import WebApp
from src.objects.displayer.ConsoleDisplayer import DisplayManager


class Displayer:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        
    def get_display(self):
        if self.test_mode:
            return DisplayManager()
        else:
            return WebApp()