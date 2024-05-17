from src.objects.SensorsChecker import SensorsChecker
from src.objects.InternetChecker import InternetChecker

from src.toolbox.Debug import Debug

from src.objects.displayer.WebDisplayer import WebApp


class Checker:
    def __init__(self) -> None:
        self.sensors_checker = SensorsChecker()
        self.internet_checker = InternetChecker()

    def check_sensors(self):
        
        Debug.LogFatSeparator("Start Checker")
        
        # datas = self.sensors_checker.check_sensors()
        # if not datas["pass"]:
        #     WebApp().show(datas["message"],"stop")
        #     Debug.LogError(datas["message"])
        #     return
        
        datas_internet = self.internet_checker.check_internet_connection()
        if not datas_internet["pass"]:
            WebApp().show(datas_internet["message"],"stop")
            Debug.LogError(datas_internet["message"])
            return
        
        Debug.LogFatSeparator("Checker done successfully !")