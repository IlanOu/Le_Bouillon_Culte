from flask import Flask, render_template, Response, url_for, request, jsonify
import threading
import logging

from src.toolbox.Debug import *

import socket

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
        self.update_event = threading.Event()
       
    def show(self, text: str):
        self.text = str(text)
        self.update_event.set()
        Debug.LogWhisper("[Display]> " + text)

class WebApp(object):
    _instance = None

    def __new__(cls, update_interval=5):
        if cls._instance is None:

            cls._instance = super(WebApp, cls).__new__(cls)
            
            ip_adress = ""
            try:
                ip_adress = cls._instance.get_ip_address()
            except:
                ip_adress = "10.42.0.1"
            
            Debug.LogSeparator(f"Server is running on : {ip_adress}:5000")
            
            cls._instance.app = Flask(__name__)
            cls._instance.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
            cls._instance.app.config['SERVER_NAME'] = f'{ip_adress}:5000'
            cls._instance.app.config['APPLICATION_ROOT'] = '/'
            cls._instance.app.config['PREFERRED_URL_SCHEME'] = 'http'
            cls._instance.string_updater = StringUpdater(update_interval)
            cls._instance.is_running = False
            cls._instance.server = None
            
            cls._instance.page_loaded = False
            

            # Removing useless logs
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

            # Redirection
            
            # Home page
            # ---------------------------------------------------------------------------- #
            @cls._instance.app.route('/')
            def home():
                
                return render_template('index.html', string=cls._instance.string_updater.text)


            # To refresh page 
            # ---------------------------------------------------------------------------- #
            @cls._instance.app.route('/stream')
            def stream():
                def generate_stream():
                    while True:
                        yield f"data: {cls._instance.string_updater.text}\n\n"
                        cls._instance.string_updater.update_event.wait()
                        cls._instance.string_updater.update_event.clear()

                return Response(generate_stream(), mimetype='text/event-stream')


            # Check if page has been loaded for client
            # ---------------------------------------------------------------------------- #
            @cls._instance.app.route('/page-loaded', methods=['POST'])
            def page_loaded_event():
                data = request.get_json()
                if data and data.get('loaded'):
                    # Enregistrer l'information de chargement de page pour l'utilisateur
                    cls._instance.page_loaded = True
                    Debug.LogWhisper("[Log]> Écran cliqué")
                    return jsonify({'message': 'La page a été chargée côté client.'})
                else:
                    return jsonify({'message': 'Erreur lors de la vérification du chargement de la page.'})
            

        return cls._instance
    
    def exit(self):
        exit(0)
        

    def get_ip_address(self):
        """
        Retourne l'adresse IP de l'appareil.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            return ip_address
        except Exception as e:
            Debug.LogError(f"Erreur lors de la récupération de l'adresse IP : {e}")
            return None

    def show(self, content, mode="text"):
        with self.app.app_context():
            image_urls = []

            if mode == "image":
                image_url = url_for('static', filename="images/" + content, _external=True)
                content = image_url
            elif mode == "3images":
                for image in content.split("|"):
                    image = image.strip()
                    Debug.LogFatSeparator("\"" + image + "\"")
                    image_url = url_for('static', filename=f"images/{image}", _external=True)
                    # image_url.replace("%20", "")
                    image_urls.append(image_url)

                content = "|".join(image_urls)

        if not self.is_running:
            self.string_updater.show(mode + "||" + content)

            self.server = threading.Thread(target=self.app.run, kwargs={'debug': False, 'use_reloader': False})
            self.server.start()
            self.is_running = True
        else:
            self.string_updater.show(mode + "||" + content)