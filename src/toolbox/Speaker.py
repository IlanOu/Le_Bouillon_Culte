from src.toolbox.Debug import *

from abc import ABC, abstractmethod


# Protocole
# ---------------------------------------------------------------------------- #
class TTSEngine(ABC):
    """
    Classe abstraite définissant l'interface pour les moteurs de synthèse vocale.
    """
    @abstractmethod
    def say(self, text: str):
        pass





# CoquiTTS
# ----------------------------------------------------------------------------
""" 
class CoquiTTSEngine(TTSEngine):
    
    # Implémentation de TTSEngine utilisant la bibliothèque coqui-tts.
    
    def say(self, text: str):
        from coqui import load_tts_model, load_tts_samples
        import os
        import tempfile
        
        model = load_tts_model("tts_models/fr/tts_model.pth")
        samples = load_tts_samples("tts_models/fr/tts_samples.txt")
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            audio = model.tts(text, samples)
            audio.save(temp_file)
            command = f"aplay {temp_file}"
            os.system(command) 
"""


class ElevenLabsEngine(TTSEngine):
    def say(self, text: str):
        from elevenlabs.client import ElevenLabs
        from elevenlabs import play, stream, save
        from dotenv import load_dotenv
        import os 
        
        
        load_dotenv()
        
        key = os.environ.get("ELEVENLABS_API_KEY")
        client = ElevenLabs(
            api_key=key
        )
        
        audio = client.generate(
            text=text,
            voice="Martin Dupont Profond", # Nicolas Petit
            model="eleven_multilingual_v2")
        
        play(audio)
        


# Pyttsx3
# ----------------------------------------------------------------------------
class Pyttsx3Engine(TTSEngine):
    """
    Implémentation de TTSEngine utilisant la bibliothèque pyttsx3.
    """
    def say(self, text: str):
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('voice', 'french')

        engine.say(text)
        engine.runAndWait()



# Simple Engine
# ----------------------------------------------------------------------------
class SimpleEngine(TTSEngine):
    
    def say(self, text:str):
        import tempfile
        import os
        
        # Créer un fichier audio temporaire
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file_name = temp_file.name

            # Générer l'audio avec pico2wave
            # text = "Bonjour, je peux parler maintenant grâce à pico2wave."
            command = f"pico2wave -l fr-FR -w {temp_file_name} '{text}' && aplay {temp_file_name}"
            os.system(command)



# Gtts
# ----------------------------------------------------------------------------
class GttsEngine(TTSEngine):
    """
    Implémentation de TTSEngine utilisant la bibliothèque Google Text-to-Speech (gTTS).
    """

    def say(self, text):
        from gtts import gTTS
        import subprocess
        import os

        # Créer un objet gTTS avec le texte et la langue
        tts = gTTS(text=text, lang='fr')

        # Enregistrer l'audio dans un fichier temporaire
        temp_file = 'temp.mp3'
        tts.save(temp_file)

        # Lire le fichier audio sur le haut-parleur
        subprocess.call(['mpg123', '-q', temp_file])

        # Supprimer le fichier temporaire
        os.remove(temp_file)



class PiperEngine(TTSEngine):
    def say(self, text: str):
        import subprocess

        text = str(text).replace("'", "")

        # Définir la commande à exécuter
        commande = "echo '" + text + "' | ./piper/piper --model ./assets/tts_models/fr_FR-upmc-medium.onnx --speaker 1 --output_file temp.wav"

        # Exécuter la commande
        process = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE)

        # Obtenir la sortie de la commande (le message audio)
        output, _ = process.communicate()

        # Vérifier si la commande a réussi
        if process.returncode == 0:
            # Ouvrir le fichier audio dans un lecteur externe
            file = "temp.wav"
            
            
            import simpleaudio as sa
            
            wave_obj = sa.WaveObject.from_wave_file(file)
            play_obj = wave_obj.play()
            play_obj.wait_done()

        else:
            Debug.LogError("Erreur lors de l'exécution de la commande:", process.returncode)



# Speaker
# ---------------------------------------------------------------------------- #
class Speaker:
    """
    Classe permettant de lire du texte à haute voix en utilisant différents moteurs de synthèse vocale.
    """
    engine = PiperEngine() # Default engine
    
    @staticmethod
    def say(text: str):
        """
        Lit le texte donné à haute voix en utilisant le moteur de synthèse vocale spécifié.
        
        Args:
            text (str): Le texte à lire.
            engine (TTSEngine, optional): Le moteur de synthèse vocale à utiliser. Par défaut, Pyttsx3Engine est utilisé.
        """
        if text == "":
            Debug.LogError("Le TTS a été appelé avec un contenu vide. Vérifiez le TTS puis réessayez.")
        
        Debug.LogColor("[TTS]> " + text, Style.ITALIC + Style.BLUE)
        Speaker.engine.say(text)
    
    @staticmethod
    def setEngine(engine: TTSEngine):
        Speaker.engine = engine
        
