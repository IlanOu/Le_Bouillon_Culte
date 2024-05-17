from src.objects.SensorsChecker import SensorsChecker
from src.toolbox.Debug import Debug


class Checker:
    def __init__(self) -> None:
        self.sensors_checker = SensorsChecker()
        

    def check_sensors(self):
        datas = self.sensors_checker.check_sensors()
        if not datas["pass"]:
            Debug.LogError(datas["message"])
            return