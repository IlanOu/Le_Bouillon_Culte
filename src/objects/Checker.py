from src.objects.SensorsChecker import SensorsChecker
from src.objects.InternetChecker import InternetChecker

from src.toolbox.Debug import Debug

from src.objects.displayer.WebDisplayer import WebApp


class Checker:
    def __init__(self) -> None:
        self.sensors_checker = SensorsChecker()
        self.internet_checker = InternetChecker()

    def check_sensors(self, server_thread):
        
        Debug.LogFatSeparator("Start Checker")

        # Check Sensors : Buttons - Screen
        # ---------------------------------------------------------------------------- #
        datas = self.sensors_checker.check_sensors(server_thread)
        if not datas["pass"]:
            WebApp().show(datas["message"], "stop")
            Debug.LogError(datas["message"])
            return

        # Check Internet
        # ---------------------------------------------------------------------------- #
        datas_internet = self.internet_checker.check_internet_connection()
        if not datas_internet["pass"]:
            WebApp().show(datas_internet["message"], "stop")
            Debug.LogError(datas_internet["message"])
            return

        Debug.LogFatSeparator("Checker done successfully !")