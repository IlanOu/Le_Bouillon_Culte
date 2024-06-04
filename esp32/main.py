from machine import Pin, SPI
import time
import mfrc522
import uwebsockets.client
import json
import sys

url = "ws://192.168.36.126:8080"

SystemState = "test"
RFIDStates = {"Auvergne-Rhône-Alpes" : False, "PACA" : False}

# Initialisation du bus SPI
spi = SPI(2, baudrate=100000, polarity=0, phase=0)

# Création des instances des broches
mosi = 13
miso = 12
sck = 14
rst = 27
cs = 15

class RFID:
    def __init__(self, sck, mosi, miso, rst, cs, name, receive_task):
        self.rdr = mfrc522.MFRC522(sck, mosi, miso, rst, cs)
        self.name = name
    
    def process(self):
        (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)

        if stat == self.rdr.OK:
            # Lecture de la carte
            (stat, uid) = self.rdr.anticoll()

            if stat == self.rdr.OK:
                print("Carte détectée")
                print("ID: %s"%str(uid))
                print("Name : " + self.name)
                data = {"action": "RFID", "data": self.name}
                dataJson = json.dumps(data)
                receive_task.send(dataJson)
                
    def test(self, timeout, start_time):
        badge_detected = False

        while not badge_detected:
            elapsed_time = time.time() - start_time  # Calcule le temps écoulé
            if elapsed_time > timeout:
                RFIDStates[self.name] = False
                print(f"{self.name} is not checked (timeout)")
                print(RFIDStates)
                
                break

            (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)

            if stat == self.rdr.OK:
                # Lecture de la carte
                (stat, uid) = self.rdr.anticoll()

                if stat == self.rdr.OK:
                    RFIDStates[self.name] = True
                    print(f"{self.name} is checked !!")
                    print(RFIDStates)
                    badge_detected = True
            else:
                time.sleep(0.1)  # Attend un peu avant de réessayer
                

print("Placez une carte pour la lire")

def CheckRFID(receive_task):
    timeout = 10  # Temps maximum pour badger en secondes
    start_time = time.time()  # Enregistre le temps de départ

    for rfid in RFIDChecker:
        rfid.test(timeout, start_time)
    
    all_true = True
    for value in RFIDStates.values():
        if not value:
            all_true = False
            break

    if all_true:
        SystemState = "normal"
    
    data = {"action": "checkRFID", "data": RFIDStates}
    dataJson = json.dumps(data)
    receive_task.send(dataJson)
    print("check !!!!!!!!!!!!!!!!!!")
    
connected = False
while not connected:
    try:
        receive_task = uwebsockets.client.connect(url)
        receive_task.send("Hello, server!")
        connected = True
    except Exception as e:
        print(f"Erreur lors de la connexion au serveur WebSocket : {e}")
        print("Nouvelle tentative de connexion dans 5 secondes...")
        time.sleep(1)
        
RFID1 = RFID(18, 23, 19, 22, 5, "Auvergne-Rhône-Alpes", receive_task)
RFID2 = RFID(sck, mosi, miso, rst, cs, "PACA", receive_task)

RFIDChecker = [RFID1, RFID2]

while SystemState == "test":
    data = receive_task.recv()
    if data == "test":
        print(f"Données reçues : {data}")
        # Traitez les données reçues ici
        CheckRFID(receive_task)
        break
    else:
        SystemState = "normal"


print("Je suis passé")

# Démarre la réception des données WebSocket en arrière-plan




while True:
    RFID1.process()
    RFID2.process()
    time.sleep(0.1)
