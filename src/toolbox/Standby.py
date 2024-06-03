from src.toolbox.Singleton import singleton

import time
import threading

@singleton
class StandBy:
    """
    Un timer réinitialisable qui s'exécute en arrière-plan, 
    se réinitialise à zéro après chaque exécution 
    et appelle une fonction après un délai donné.
    """

    def __init__(self, interval, function, args=None, kwargs=None):
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.timer = None
        self.is_running = False

    def start(self):
        """Démarre ou réinitialise le timer."""
        self.reset()

    def reset(self):
        """Réinitialise le timer à zéro."""
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.interval, self._timer_complete)
        self.timer.start()
        self.is_running = True

    def _timer_complete(self):
        """Fonction appelée lorsque le timer est terminé."""
        self.is_running = False
        self.function(*self.args, **self.kwargs)
        self.reset()  # Réinitialise le timer pour la prochaine exécution

    def cancel(self):
        """Annule le timer s'il est en cours d'exécution."""
        if self.timer:
            self.timer.cancel()
            self.is_running = False

# Exemple d'utilisation:
def action():
    print("5 minutes se sont écoulées !")

# Créer un timer qui se déclenche toutes les 5 minutes (300 secondes)
timer = StandBy(3, action)

# Démarrer le timer
timer.start()

# ... votre programme continue ...

# Vous pouvez vérifier si le timer est en cours d'exécution avec timer.is_running
# Vous pouvez arrêter le timer avec timer.cancel()