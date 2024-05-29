from src.toolbox.Debug import Debug, Style
from src.objects.button.Button import Button

from src.Config import Config

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import threading

from src.toolbox.Singleton import singleton


# Sensors Manager
# ---------------------------------------------------------------------------- #

@singleton
class SensorsManager:
    def __init__(self):
        self.buttons = [Button(pin) for pin in Config().buttons_pins]
        self.RFID = SimpleMFRC522()
        
        self.waiting_for_button = False
        self.stop_event = threading.Event()
        

    def read_rfid(self):
        id, text = self.RFID.read()
        return id, text

    def wait_for_read_rfid(self):
        self.waiting_for_RFID = True
        self.rfid_result = None
        self.stop_event.clear()  # Réinitialiser l'événement

        # Lancer la lecture RFID dans un thread séparé
        rfid_thread = threading.Thread(target=self.read_rfid_with_timeout)
        rfid_thread.start()

        # Attendre le résultat ou le délai d'expiration
        rfid_thread.join(timeout=5)  # Attendre 5 secondes maximum

        self.stop_event.set()  # Signaler l'arrêt du thread
        self.waiting_for_RFID = False

        # Retourner le résultat ou None si le délai est dépassé
        return self.rfid_result

    def read_rfid_with_timeout(self):
        try:
            self.rfid_result = self.read_rfid()
            self.stop_event.set()  # Signaler l'arrêt du thread si un scan est effectué
        except Exception as e:
            print(f"Erreur lors de la lecture RFID : {e}")
        finally:
            self.stop_event.set()  # Signaler l'arrêt du thread dans tous les cas

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