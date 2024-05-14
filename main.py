# ----------------------------------- Main ----------------------------------- #
""" 
from src.Application import App

if __name__ == "__main__":
    app = App()
    app.run()
 """

# ----------------------------------- Test ----------------------------------- #
""" 
from src.toolbox.Speaker import *

Speaker.say("Salut, je suis un texte de test ! Je parles parfaitement bien !", ElevenLabsEngine()) 
"""


from src.toolbox.Websocket import *
from src.objects.joystick.StateJoystick import *
from src.toolbox.Debug import Debug, Style

server = WebSocketServer("0.0.0.0", 8080)
server.start()

while Joystick.get_current_state() == StateJoystick.UP:
    pass

Debug.LogColor("Pour vouvez lancer la suite", Style.PURPLE + Style.ITALIC)


import mfrc522
from machine import Pin, SPI
sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
spi = SPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

sda = Pin(5, Pin.OUT)