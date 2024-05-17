from src.objects.SensorsChecker import SensorsChecker
from src.toolbox.Debug import Debug


class Checker:
    def __init__(self) -> None:
        self.sensors_checker = SensorsChecker()
        

    def checkSensors(self):
        datas = self.sensors_checker.checkSensors()
        if not datas["pass"]:
            Debug.LogError(datas["message"])
            return