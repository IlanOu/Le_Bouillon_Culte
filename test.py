import os
import random
from pygame import mixer, pygame
import threading
import time

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        mixer.init()
        self.current_music = None
        self.last_stop_time = None
        self.sound_thread = None

    def get_audio_files(self):
        return [f for f in os.listdir(self.music_dir) if f.endswith(".mp3") or f.endswith(".wav")]

    def play(self, audio_file: str, duration=None):
        music_file_path = os.path.join(self.music_dir, audio_file)
        
        # Debug.LogPopup(music_file_path)
        
        mixer.music.load(music_file_path)
        mixer.music.play()

        if duration == None:
            duration = mixer.Sound(music_file_path).get_length()

        time.sleep(duration)

        mixer.music.stop()

    def play_threading(self, audio_file: str, duration=None):
          """Joue un son dans un thread séparé.

          Args:
              audio_file (str): Le nom du fichier audio.
              duration (int, optional): Durée de lecture en secondes. 
                                          Si None, joue la piste entière.
          """
          music_file_path = os.path.join(self.music_dir, audio_file)

          if not os.path.isfile(music_file_path):
              # Debug.LogWarning(f"Le fichier {audio_file} n'existe pas dans le dossier.")
              return

          def play_sound_thread():
              try:
                  mixer.music.load(music_file_path)
                  mixer.music.play()

                  if duration is None:
                      duration = mixer.Sound(music_file_path).get_length()

                  time.sleep(duration)
                  mixer.music.stop()

              except pygame.error as e:
                  # Debug.LogWarning(f"Erreur lors de la lecture du son: {e}")
                  pass

          # Arrêter le thread précédent s'il est toujours en cours d'exécution
          if self.sound_thread and self.sound_thread.is_alive():
              self.sound_thread.join()

          self.sound_thread = threading.Thread(target=play_sound_thread)
          self.sound_thread.start()
        

    def play_random_section(self, music_file, duration=10):
        music_file_path = os.path.join(self.music_dir, music_file)

        if not os.path.isfile(music_file_path):
            # Debug.LogWarning(f"Le fichier {music_file} n'existe pas dans le dossier.")
            return

        mixer.music.load(music_file_path)
        self.current_music = music_file_path
        self.last_stop_time = None

        # Obtenir la durée totale de la musique
        music_length = mixer.Sound(music_file_path).get_length()

        # Choisir un temps de départ aléatoire
        start_time = random.uniform(0, music_length - duration*2)

        mixer.music.play(start=start_time)

        time.sleep(duration)

        mixer.music.stop()
        self.last_stop_time = start_time + duration

    def play_next_random_section(self, duration=10):
        if self.current_music is None or self.last_stop_time is None:
            # Debug.LogWarning("Aucune musique en cours de lecture ou pas de temps d'arrêt précédent.")
            return

        music_file_path = self.current_music

        # Obtenir la durée totale de la musique
        music_length = mixer.Sound(music_file_path).get_length()

        # Calculer le nouveau temps de départ à partir du dernier temps d'arrêt
        start_time = self.last_stop_time

        mixer.music.load(music_file_path)
        mixer.music.play(start=start_time)

        time.sleep(duration)

        mixer.music.stop()
        self.last_stop_time = start_time + duration
        
music_dir = "/assets/audio"
player = MusicPlayer(music_dir)
music_file = "0.mp3"
player.play_threading(music_file)
