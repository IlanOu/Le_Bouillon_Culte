from src.objects.SensorsManager import SensorsManager
from src.objects.button.Button import Button
from src.Config import Config
import threading
import time
from src.toolbox.Debug import Debug, Style

from websocket_server import WebsocketServer

class SensorsChecker:
    def __init__(self):
        self.buttons_pin = [16]
        self.sensors_manager = SensorsManager()
        self.timer = None
        
        self.buttons_error = False
        self.buttons_pin_error = None
        self.time_to_press = 10
        self.web_app_loaded = False

    # Main Checker
    # ---------------------------------------------------------------------------- #
    def check_sensors(self):
        
        # Check Buttons
        # ---------------------------------------------------------------------------- #
        # self.check_buttons()
        
        # if self.buttons_error:
        #     return {"pass": False, "message": f"Le bouton avec le pin {self.buttons_pin_error} ne fonctionne pas."}


        self.check_RFIDs()

        # Check WebApp
        # ---------------------------------------------------------------------------- #
        # web_app_data = self.check_displayer()
        
        # if not web_app_data:
        #     return {"pass": False, "message": "Temps d'attente dépassé pour charger la page web."}
        
        
        # return {"pass": True, "message": ""}
        
        
        
    # RFID Checker
    # ---------------------------------------------------------------------------- #
    def check_RFIDs(self):
        WebsocketServer.addCallback(didReceiveMessagee)
        print()
        WebsocketServer.send_message_to_all(WebsocketServer.handler_mask_key, "launch")
    
    def didReceiveMessagee(self, message):
        print(message)
    
    # Displayer checker
    # ---------------------------------------------------------------------------- #
    def check_displayer(self):
        Config().webApp.show("Cliquez sur l'écran")
        Debug.LogColor("[Action]> Cliquez sur l'écran", Style.PURPLE + Style.ITALIC)
        
        self.web_app_loaded = False
        self.timer = threading.Timer(self.time_to_press, self.handle_web_app_timeout)
        self.timer.start()
        
        # Attendre que la page web soit chargée ou que le délai expire
        while not Config().webApp.page_loaded and self.timer.is_alive():
            time.sleep(0.1)  # Éviter d'utiliser trop de ressources processeur
        
        self.timer.cancel()
        return Config().webApp.page_loaded

    def handle_web_app_timeout(self):
        self.web_app_loaded = False


    # Button Checker
    # ---------------------------------------------------------------------------- #
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