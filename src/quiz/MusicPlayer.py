import os
import random
from pygame import mixer

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        mixer.init()
        self.current_music = None
        self.last_stop_time = None

    def get_audio_files(self):
        return [f for f in os.listdir(self.music_dir) if f.endswith(".mp3") or f.endswith(".wav")]

    def play_random_section(self, music_file, duration=10):
        music_file_path = os.path.join(self.music_dir, music_file)

        if not os.path.isfile(music_file_path):
            print(f"Le fichier {music_file} n'existe pas dans le dossier.")
            return

        mixer.music.load(music_file_path)
        self.current_music = music_file_path
        self.last_stop_time = None

        # Obtenir la durée totale de la musique
        music_length = mixer.Sound(music_file_path).get_length()

        # Choisir un temps de départ aléatoire
        start_time = random.uniform(0, music_length - duration*2)

        mixer.music.play(start=start_time)

        import time
        time.sleep(duration)

        mixer.music.stop()
        self.last_stop_time = start_time + duration

    def play_next_random_section(self, duration=10):
        if self.current_music is None or self.last_stop_time is None:
            print("Aucune musique en cours de lecture ou pas de temps d'arrêt précédent.")
            return

        music_file_path = self.current_music

        # Obtenir la durée totale de la musique
        music_length = mixer.Sound(music_file_path).get_length()

        # Calculer le nouveau temps de départ à partir du dernier temps d'arrêt
        start_time = self.last_stop_time

        mixer.music.load(music_file_path)
        mixer.music.play(start=start_time)

        import time
        time.sleep(duration)

        mixer.music.stop()
        self.last_stop_time = start_time + duration

# # Exemple d'utilisation
# music_dir = "/chemin/vers/le/dossier/musique"
# player = MusicPlayer(music_dir)
# music_file = "nom_du_fichier_audio.mp3"
# player.play_random_section(music_file)
# player.play_next_random_section()