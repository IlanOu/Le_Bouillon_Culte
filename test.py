from src.Config import Config
from src.objects.SensorsManager import SensorsManager
from src.Config import Config

import threading

class StandBy:
    """
    Un timer réinitialisable qui s'exécute en arrière-plan, 
    se réinitialise à zéro après chaque exécution 
    et appelle une fonction après un délai donné.
    """

    def __init__(self, args=None, kwargs=None):
        self.interval = 3
        self.sensor_manager = SensorsManager()
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
        self._active_standby()
        self.reset()  # Réinitialise le timer pour la prochaine exécution
        
    def _active_standby(self):
      Config().webApp.show("", "text")
      self.sensor_manager.wait_for_button_press(Config().button_start)
      

    def cancel(self):
        """Annule le timer s'il est en cours d'exécution."""
        if self.timer:
            self.timer.cancel()
            self.is_running = False

# Créer un timer qui se déclenche toutes les 5 minutes (300 secondes)
StandBy().start()