from src.toolbox.Debug import Debug
from src.objects.button.Button import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

from src.objects.Displayer.WebDisplayer import WebApp

class SensorsManager:
    def __init__(self, button_pins=[16]):
        self.buttons = [Button(pin) for pin in button_pins]
        self.RFID = SimpleMFRC522()
        self.webApp = WebApp(update_interval=1)

    def read_rfid(self):
        Debug.LogWhisper("Passez le badge devant le capteur RFID...")
        self.webApp.show("Placez le pion sur la carte")
        
        id, text = self.RFID.read()
        return id, text

    def wait_for_button_press(self):
        Debug.LogWhisper("Appuyez sur un bouton svp...")
        
        for button in self.buttons:
            button.setup_button()
        
        while True:
            for button in self.buttons:
                if button.process():
                    Debug.LogWhisper(f"Pin du bouton pressé: {button.pin}")
                    return button.pin
            time.sleep(0.1)

    def cleanup(self):
        GPIO.cleanup()