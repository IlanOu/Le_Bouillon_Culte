from src.Config import Config
from src.toolbox.Debug import *
import time

Debug.prefixActive = False



Config().webApp.show("Choisissez le nombre de questions : ~ 5 | 7 | 10 | 12", "table")

time.sleep(3)

Config().webApp.show("Placez le pion sur la carte")

time.sleep(2)

Config().webApp.show("C5_SE_2.jpg", "image")

time.sleep(1)

Debug.LogError("Erreur")


