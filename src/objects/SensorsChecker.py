from src.objects.SensorsManager import SensorsManager
from src.objects.button.Button import Button
from src.Config import Config
import threading
import time
from src.toolbox.Debug import Debug, Style

from websocket_server import WebsocketServer

class SensorsChecker:
    def __init__(self):
        self.buttons_pin = Config().buttons_pins
        self.sensors_manager = SensorsManager()
        self.timer = None
        
        self.buttons_error = False
        self.buttons_pin_error = None
        self.rfid_response = None
        self.rfid_error = False
        self.rfid_zone_error = []
        self.time_to_press = 10
        self.web_app_loaded = False

    # Main Checker
    # ---------------------------------------------------------------------------- #
    def check_sensors(self, server_thread):

        server_thread.addCallbackTest(self.receive_message)

        
        # Check Buttons
        # ---------------------------------------------------------------------------- #
        for pin in Config().buttons_pins:
            self.check_button(pin)
        
        if self.buttons_error:
            return {"pass": False, "message": f"Le bouton avec le pin {self.buttons_pin_error} ne fonctionne pas."}


        # Check RFID
        # ---------------------------------------------------------------------------- #
        self.check_RFIDs(server_thread)

        if self.rfid_error:
            return {"pass": False, "message": f"Le(s) RFID avec le(s) {self.rfid_zone_error} ne fonctionne pas."}
            if self.buttons_error:
                return {"pass": False, "message": f"Le bouton avec le pin {self.buttons_pin_error} ne fonctionne pas."}
 

        # Check WebApp
        # ---------------------------------------------------------------------------- #
        web_app_data = self.check_displayer()
        
        if not web_app_data:
            return {"pass": False, "message": "Temps d'attente dépassé pour charger la page web."}
        
        return {"pass": True, "message": ""}


    def receive_message(self, message):
        print(f"Message reçu dans SensorsChecker : {message}")
        self.rfid_response = message

    # RFID Checker
    # ---------------------------------------------------------------------------- #
    def check_RFIDs(self, server_thread):
        self.rfid_response = None
        self.all_wait_rfid = False
        self.all_rfid = {}

        self.rfid_result = self.sensors_manager.wait_for_read_rfid()

        if self.rfid_result is not None:
            self.all_rfid["Bretagne"] = True
        else:
            self.all_rfid["Bretagne"] = False

        print("J'envoie le test !!!!!")

        server_thread.send_message_to_all("test")

        # Attendre la réponse pendant 10 secondes maximum
        while self.all_wait_rfid is False:
            while self.rfid_response is None:
                time.sleep(0.1)
                
                
            key = self.rfid_response.keys()

            for zone in key :
                self.all_rfid[zone] = self.rfid_response[zone]

            print("Voici le self.all_rfid : " + str(self.all_rfid))

            if len(self.all_rfid) == 5:
                self.all_wait_rfid = True
            
            self.rfid_response = None
            

        allKey = self.all_rfid.keys()

        for zone in allKey :
            if self.all_rfid[zone] == False :
                self.rfid_zone_error.append(zone)
                self.rfid_error = True

        return     

        


    
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
    def check_button(self, button_pin):
        Config().webApp.show("Appuyez sur le bouton " + str(button_pin))
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