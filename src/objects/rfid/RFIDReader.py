from src.toolbox.Debug import Debug, Style
from src.objects.button.Button import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

class RFIDReader:
    def __init__(self):
        self.button = Button(16)
        self.MIFAREReader = SimpleMFRC522()

    def read_rfid(self):
        Debug.LogWhisper("Passez le badge devant le capteur RFID...")
        id, text = self.MIFAREReader.read()
        return id, text

    def wait_for_button_press(self):
        Debug.LogWhisper("Appuyez sur le bouton svp...")
        button_pressed = False
        while not button_pressed:
            button_pressed = self.button.process()
            time.sleep(0.1)

    def cleanup(self):
        GPIO.cleanup()
