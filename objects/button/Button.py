import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def process(self):
        button_state = GPIO.input(self.pin)
        if button_state == GPIO.LOW:
            print("Bouton pressé")
            return True
        else:
            return False



