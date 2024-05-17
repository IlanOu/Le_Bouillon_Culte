from src.toolbox.Debug import Debug, Style
from src.objects.button.Button import Button

from src.Config import Config

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

from src.toolbox.Singleton import singleton


# Sensors Manager
# ---------------------------------------------------------------------------- #

@singleton
class SensorsManager:
    def __init__(self, button_pins=[16]):
        self.buttons = [Button(pin) for pin in button_pins]
        self.RFID = SimpleMFRC522()
        
        self.waiting_for_button = False
        self.waiting_for_RFID = False

    def read_rfid(self):
        Debug.LogColor("[Action]> Passez le badge devant le capteur RFID...", Style.PURPLE + Style.ITALIC)
        Config().webApp.show("Placez le pion sur la carte")
        
        id, text = self.RFID.read()
        return id, text

    def wait_for_button_press(self, button=None):
        self.waiting_for_button = True
        if button == None:
            Debug.LogColor("[Action]> Appuyez sur un bouton svp...", Style.PURPLE + Style.ITALIC)
            
            for button in self.buttons:
                button.setup_button()
            
            while self.waiting_for_button:
                for button in self.buttons:
                    if button.process():
                        Debug.LogWhisper(f"[Log]> Pin du bouton pressé: {button.pin}")
                        return button.pin
                time.sleep(0.1)
        else:
            Debug.LogColor(f"[Action]> Appuyez sur le bouton {button.pin} svp...", Style.PURPLE + Style.ITALIC)
            
            button.setup_button()
            
            while self.waiting_for_button:
                if button.process():
                    Debug.LogWhisper(f"[Log]> Pin du bouton pressé: {button.pin}")
                    return button.pin
                time.sleep(0.1)
                
    def stop_waiting_for_buttons(self):
        self.waiting_for_button = False

    def cleanup(self):
        GPIO.cleanup()