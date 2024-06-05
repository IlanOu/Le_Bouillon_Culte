import os
import random
import pygame
import threading
import time

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        pygame.mixer.init()
        self.current_music = None
        self.last_stop_time = None
        self.sound_thread = None

    def play_threading(self, audio_file: str):
        """Joue un son dans un thread séparé.

        Args:
            audio_file (str): Le nom du fichier audio.
            duration (int, optional): Durée de lecture en secondes. 
                                        Si None, joue la piste entière.
        """
        music_file_path = os.path.join(self.music_dir, audio_file)

        if not os.path.isfile(music_file_path):
            print(f"Le fichier {audio_file} n'existe pas dans le dossier.")
            return

        def play_sound_thread():
            try:
                pygame.mixer.music.load(music_file_path)
                pygame.mixer.music.play()

                duration = pygame.mixer.Sound(music_file_path).get_length()

                time.sleep(duration)
                pygame.mixer.music.stop()

            except pygame.error as e:
                print(f"Erreur lors de la lecture du son: {e}")
                pass

        # Arrêter le thread précédent s'il est toujours en cours d'exécution
        if self.sound_thread and self.sound_thread.is_alive():
            self.sound_thread.join()

        self.sound_thread = threading.Thread(target=play_sound_thread)
        self.sound_thread.start()
        
        
music_dir = "./assets/audio"
player = MusicPlayer(music_dir)
music_file = "sounds/0.mp3"
player.play_threading(music_file)
