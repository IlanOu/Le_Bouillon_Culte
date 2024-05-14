import time
import random
import math
from src.toolbox.Debug import Debug

from src.Config import Config

class RollingNumberDisplay:
    def __init__(self, numbers, target_number, num_rolls=3):
        self.numbers = numbers
        self.target_number = target_number
        self.num_rolls = num_rolls
        self.initial_delay = 0.05  # Délai initial (rapide)
        self.final_delay = 0.5  # Délai final (ralenti)

    def display_rolling_number(self):
        Config().webApp.show("", "roll")
        time.sleep(2)
        for roll in range(self.num_rolls):
            if roll == self.num_rolls - 1:
                self.roll_numbers_with_slowdown()
            else:
                self.roll_numbers()
            # time.sleep(1)  # Pause entre les tours

    def roll_numbers(self):
        # Afficher les nombres de manière aléatoire
        while True:
            current_number = random.choice(self.numbers)
            Config().webApp.show(str(current_number), "roll")
            time.sleep(self.initial_delay)

            # Arrêter le défilement lorsque le nombre cible est atteint
            if current_number == self.target_number:
                break

    def roll_numbers_with_slowdown(self):
        # Afficher les nombres de manière aléatoire avec ralentissement
        delay = self.initial_delay
        num_steps = len(self.numbers) - 1
        if num_steps > 0:
            for i in range(num_steps + 1):
                current_number = random.choice(self.numbers)
                Config().webApp.show(str(current_number), "roll")

                # Calculer le nouveau délai avec une fonction exponentielle modifiée
                delay = self.initial_delay + (self.final_delay - self.initial_delay) * (1 - math.exp(-(i / num_steps)**2))

                time.sleep(delay)

                # Afficher le nombre cible si c'est la dernière itération
                if i == num_steps:
                    current_number = self.target_number

        time.sleep(0.5)
        # Afficher le nombre cible une dernière fois après le ralentissement
        Config().webApp.show(str(self.target_number), "roll")
        Debug.LogWhisper("[Log]> " + self.target_number)


"""
# Exemple d'utilisation
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target_number = 7
num_rolls = 3

rolling_display = RollingNumberDisplay(numbers, target_number, num_rolls)
rolling_display.display_rolling_number()
"""