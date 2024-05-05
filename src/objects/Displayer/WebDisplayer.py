from flask import Flask, render_template, Response
import time
import threading
import logging



"""

Lancer le WebDisplayer :

webApp = WebApp(update_interval=1) # initialiser le displayer
webApp.show("Le texte que l'on veut") # Pour afficher le texte que l'on veut 

webApp.show("Le texte que /n l'on veut") # Pour afficher le texte que l'on veut avec un retour à la ligne [ Attention c'est un /n, pas un \n ! ] 


Afficher un tableau :

webApp.show("A | B | C | D") # Tableau simple 
webApp.show("Titre ~ A | B | C | D") # Tableau avec un titre 


"""


class StringUpdater:
    def __init__(self, update_interval=5):
        self.text = "..."
        self.update_interval = update_interval

    def show(self, text: str):
        self.text = str(text)

    def start_updater(self):
        thread = threading.Thread(target=self._update_and_stream)
        thread.daemon = True
        thread.start()

    def _update_and_stream(self):
        while True:
            time.sleep(self.update_interval)


class WebApp(object):
    _instance = None

    def __new__(cls, update_interval=5):
        if cls._instance is None:
            
            cls._instance = super(WebApp, cls).__new__(cls)
            cls._instance.app = Flask(__name__)
            cls._instance.string_updater = StringUpdater(update_interval)
            cls._instance.is_running = False
            
            # Removing useless logs
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

            # Redirection
            @cls._instance.app.route('/')
            def home():
                return render_template('index.html', string=cls._instance.string_updater.text)

            @cls._instance.app.route('/stream')
            def stream():
                def generate_stream():
                    while True:
                        yield f"data: {cls._instance.string_updater.text}\n\n"
                        time.sleep(cls._instance.string_updater.update_interval)
                        
                
                return Response(generate_stream(), mimetype='text/event-stream')

        return cls._instance

    def show(self, text):
        if not self.is_running:
            self.string_updater.show(text)
            self.string_updater.start_updater()
            
            threading.Thread(target=self.app.run, kwargs={'debug': False, 'use_reloader': False}).start()
            self.is_running = True
        else:
            self.string_updater.show(text)

