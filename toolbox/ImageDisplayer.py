# import pygame

# def display_image(image_path, x, y):
#     """
#     Affiche une image à une position spécifique sur l'écran.

#     Args:
#         image_path (str): Chemin d'accès au fichier image.
#         x (int): Coordonnée x de la position de l'image.
#         y (int): Coordonnée y de la position de l'image.
#     """
#     pygame.init()

#     # Obtenir les dimensions de l'écran
#     screen_info = pygame.display.Info()
#     screen_width, screen_height = screen_info.current_w, screen_info.current_h

#     # Créer une fenêtre de la taille de l'écran
#     screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

#     # Charger l'image
#     image = pygame.image.load(image_path)

#     # Obtenir les dimensions de l'image
#     image_width, image_height = image.get_size()

#     # Calculer la position de l'image en tenant compte des dimensions de l'écran
#     image_x = x
#     image_y = y

#     # Boucle principale
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#         # Effacer l'écran
#         screen.fill((0, 0, 0))

#         # Afficher l'image à la position spécifiée
#         screen.blit(image, (image_x, image_y))

#         # Mettre à jour l'affichage
#         pygame.display.flip()

#     pygame.quit()

# # Exemple d'utilisation
# # display_image("chemin/vers/image.png", 100, 200)

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap
import sys

def display_image(image_path, x, y):
    app = QApplication(sys.argv)
    label = QLabel()
    pixmap = QPixmap(image_path)
    label.setPixmap(pixmap)
    label.move(x, y)
    label.showFullScreen()
    sys.exit(app.exec_())

# Exemple d'utilisation
# display_image("chemin/vers/image.png", 100, 200)