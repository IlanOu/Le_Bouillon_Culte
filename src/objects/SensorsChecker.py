from src.objects.SensorsManager import SensorsManager
from src.objects.button.Button import Button
import threading


class SensorsChecker:
    def __init__(self):
        self.buttons_pin = [16]
        self.sensors_manager = SensorsManager()
        self.timer = None
        
        self.buttons_error = False
        self.buttons_pin_error = None
        self.time_to_press = 10

    def check_sensors(self):
        while self.buttons_error == False:
            self.check_buttons()
            break
        
        datas_to_send = {}
        
        if self.buttons_error:
            datas_to_send = {"pass": False, "message": f"Le bouton avec le pin {self.buttons_pin_error} ne fonctionne pas."}
        else:
            datas_to_send = {"pass": True, "message": ""}
        
        return datas_to_send

    def check_RFIDs(self):
        pass

    def check_buttons(self):
        for button_pin in self.buttons_pin:
            button = Button(button_pin)
            self.timer = threading.Timer(self.time_to_press, self.handle_timeout, args=[button_pin])
            self.timer.start()
            self.sensors_manager.wait_for_button_press(button=button)
            self.timer.cancel()
            return

    def handle_timeout(self, pin_button):
        self.buttons_error = True
        self.buttons_pin_error = pin_button
        self.sensors_manager.stop_waiting_for_buttons()