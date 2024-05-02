
# Using simple MFRC522

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

# Créer une instance du module RFID
MIFAREReader = SimpleMFRC522()

# Bienvenue
print("Lecture de cartes RFID")

# Cette boucle détecte les cartes RFID
try:
    while True:
        print("Lecture en cours...")
        print(MIFAREReader.read())
        id, text = MIFAREReader.read()
        
        print("id : ")
        print(id)
        print("text : ")
        print(text)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()


"""

# Using MFRC522

import RPi.GPIO as GPIO
from mfrc522 import MFRC522

# Créer une instance du module RFID
MIFAREReader = MFRC522(bus=0, device=0)

# Bienvenue
print("Lecture de cartes RFID...")

# Cette boucle détecte les cartes RFID
try:
    while True:
        # Attendre qu'une carte soit détectée
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Si une carte est détectée
        if status == MIFAREReader.MI_OK:
            print("Carte détectée")

        # Faire quelque chose quand une carte est détectée...

except KeyboardInterrupt:
    GPIO.cleanup()
"""
