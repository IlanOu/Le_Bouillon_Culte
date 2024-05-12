import RPi.GPIO as GPIO
from src.toolbox.Debug import Debug

class Button:
    def __init__(self, pin):
        self.pin = pin
        self.setup_button()

    def setup_button(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def process(self):
        button_state = GPIO.input(self.pin)
        if button_state == GPIO.LOW:
            Debug.LogWhisper("[Log]> Bouton pressé")
            return True
        else:
            return False



