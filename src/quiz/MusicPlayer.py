import os
import random
import pygame
import time
import threading

from src.toolbox.Singleton import singleton
from src.toolbox.Debug import Debug


@singleton
class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        pygame.mixer.init()
        self.current_music = None
        self.last_stop_time = None
        self.sound_thread = None

    def get_audio_files(self):
        return [f for f in os.listdir(self.music_dir) if f.endswith(".mp3") or f.endswith(".wav")]

    def play(self, audio_file: str, duration=None):
        music_file_path = os.path.join(self.music_dir, audio_file)
        
        Debug.LogPopup(music_file_path)
        
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.play()

        if duration == None:
            duration = pygame.mixer.Sound(music_file_path).get_length()

        time.sleep(duration)
        
        
        for i in range(10, 0, -1):
            pygame.mixer.music.set_volume(i/10)
            time.sleep(0.1)

        pygame.mixer.music.stop()

    def play_threading(self, audio_file: str):
        """Joue un son dans un thread séparé.

        Args:
            audio_file (str): Le nom du fichier audio.
            duration (int, optional): Durée de lecture en secondes. 
                                        Si None, joue la piste entière.
        """
        music_file_path = os.path.join(self.music_dir, audio_file)

        if not os.path.isfile(music_file_path):
            Debug.LogWarning(f"Le fichier {audio_file} n'existe pas dans le dossier.")
            return

        def play_sound_thread():
            try:
                duration = pygame.mixer.Sound(music_file_path).get_length()
                
                pygame.mixer.music.load(music_file_path)
                pygame.mixer.music.play()
                Debug.LogPopup("Play -> " + music_file_path)
                
                time.sleep(duration)

                pygame.mixer.music.stop()

            except pygame.error as e:
                Debug.LogWarning(f"Erreur lors de la lecture du son: {e}")

        # Arrêter le thread précédent s'il est toujours en cours d'exécution
        if self.sound_thread and self.sound_thread.is_alive():
            self.sound_thread.join()

        self.sound_thread = threading.Thread(target=play_sound_thread)
        self.sound_thread.start()
        

    def play_random_section(self, music_file, duration=10):
        music_file_path = os.path.join(self.music_dir, music_file)

        if not os.path.isfile(music_file_path):
            Debug.LogWarning(f"Le fichier {music_file} n'existe pas dans le dossier.")
            return

        pygame.mixer.music.load(music_file_path)
        self.current_music = music_file_path
        self.last_stop_time = None

        # Obtenir la durée totale de la musique
        music_length = pygame.mixer.Sound(music_file_path).get_length()

        # Choisir un temps de départ aléatoire
        start_time = random.uniform(0, music_length - duration*2)
        
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(start=start_time)

        time.sleep(duration)
        
        for i in range(10, 0, -1):
            pygame.mixer.music.set_volume(i/10)
            time.sleep(0.1)

        pygame.mixer.music.stop()
        self.last_stop_time = start_time + duration

    def play_next_random_section(self, duration=10):
        if self.current_music is None or self.last_stop_time is None:
            Debug.LogWarning("Aucune musique en cours de lecture ou pas de temps d'arrêt précédent.")
            return

        music_file_path = self.current_music

        # Obtenir la durée totale de la musique
        music_length = pygame.mixer.Sound(music_file_path).get_length()

        # Calculer le nouveau temps de départ à partir du dernier temps d'arrêt
        start_time = self.last_stop_time
        
        pygame.mixer.music.set_volume(1)
        
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.play(start=start_time)

        time.sleep(duration)
        for i in range(10, 0, -1):
            pygame.mixer.music.set_volume(i/10)
            time.sleep(0.1)
        pygame.mixer.music.stop()
        self.last_stop_time = start_time + duration

# # Exemple d'utilisation
# music_dir = "/chemin/vers/le/dossier/musique"
# player = MusicPlayer(music_dir)
# music_file = "nom_du_fichier_audio.mp3"
# player.play_random_section(music_file)
# player.play_next_random_section()