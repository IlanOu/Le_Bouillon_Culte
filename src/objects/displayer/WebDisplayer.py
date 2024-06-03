from flask import Flask, render_template, Response, url_for, request, jsonify
import threading
import logging

from src.toolbox.Debug import *
from src.toolbox.Singleton import singleton

from src.Config import Config

import socket


class StringUpdater:
    def __init__(self):
        self.content = []
        self.update_event = threading.Event()
       
    def show(self, content):
        self.content = content
        self.update_event.set()
        Debug.LogWhisper("[Display]> " + str(jsonify(content)))



@singleton
class WebApp(object):
    def __init__(self):
            
        ip_adress = ""
        try:
            ip_adress = WebApp().get_ip_address()
        except:
            ip_adress = Config().hotspot_ip
        
        Debug.LogSeparator(f"Server is running on : {ip_adress}:5000")
        
        WebApp().app = Flask(__name__)
        WebApp().app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        WebApp().app.config['SERVER_NAME'] = f'{ip_adress}:5000'
        WebApp().app.config['APPLICATION_ROOT'] = '/'
        WebApp().app.config['PREFERRED_URL_SCHEME'] = 'http'
        WebApp().string_updater = StringUpdater()
        WebApp().is_running = False
        WebApp().server = None
        
        WebApp().page_loaded = False
        

        # Removing useless logs
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        
        # Home page
        # ---------------------------------------------------------------------------- #
        @WebApp().app.route('/')
        def home():
            return render_template('index.html')


        # To refresh page 
        # ---------------------------------------------------------------------------- #
        @WebApp().app.route('/stream')
        def stream():
            def generate_stream():
                while True:
                    yield f"data: {jsonify(WebApp().string_updater.content).get_json()}\n\n"  # Envoyer le contenu JSONifié
                    WebApp().string_updater.update_event.wait()
                    WebApp().string_updater.update_event.clear()

            return Response(generate_stream(), mimetype='text/event-stream')


        # Check if page has been loaded for client
        # ---------------------------------------------------------------------------- #
        @WebApp().app.route('/page-loaded', methods=['POST'])
        def page_loaded_event():
            data = request.get_json()
            if data and data.get('loaded'):
                # Enregistrer l'information de chargement de page pour l'utilisateur
                WebApp().page_loaded = True
                Debug.LogWhisper("[Log]> Écran cliqué")
                return jsonify({'message': 'La page a été chargée côté client.'})
            else:
                return jsonify({'message': 'Erreur lors de la vérification du chargement de la page.'})
            

    
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

    def show(self, content):
        if not self.is_running:
            self.string_updater.show(content)

            self.server = threading.Thread(target=self.app.run, kwargs={'debug': False, 'use_reloader': False})
            self.server.start()
            self.is_running = True
        else:
            self.string_updater.show(content)