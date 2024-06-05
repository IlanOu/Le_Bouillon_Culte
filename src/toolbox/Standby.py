from src.toolbox.Singleton import singleton
from src.Config import Config
from src.objects.SensorsManager import SensorsManager
from src.Config import Config

import threading

from src.objects.button.Button import Button

@singleton
class StandBy:
    """
    Un timer réinitialisable qui s'exécute en arrière-plan, 
    se réinitialise à zéro après chaque exécution 
    et appelle une fonction après un délai donné.
    """

    def __init__(self, args=None, kwargs=None):
        
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
        self.timer = threading.Timer(Config().time_before_sleep, self._timer_complete)
        self.timer.start()
        self.is_running = True

    def _timer_complete(self):
        """Fonction appelée lorsque le timer est terminé."""
        self.is_running = False
        self._active_standby()
        self.reset()  # Réinitialise le timer pour la prochaine exécution

    def _active_standby(self):
        object = [{
                "type": "standby",
                "content": "VEILLE",
                "style": ["text-black"]
            }]
        Config().webApp.show(object)
        
        self.sensor_manager.wait_for_button_press(Button(Config().button_start))
        self.reset()
        
        Config().webApp.show_historic()


    def cancel(self):
        """Annule le timer s'il est en cours d'exécution."""
        if self.timer:
            self.timer.cancel()
            self.is_running = False

# Créer un timer qui se déclenche toutes les 5 minutes (300 secondes)
StandBy().start()