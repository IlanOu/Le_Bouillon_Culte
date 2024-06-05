from flask import Flask, render_template, Response, request, jsonify, url_for
import threading
import logging
from src.toolbox.Debug import *
from src.Config import Config
import socket
import json

class StringUpdater:
    def __init__(self):
        self.text = ""
        self.update_event = threading.Event()
       
    def show(self, text):
        self.text = text
        self.update_event.set()

class WebApp(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebApp, cls).__new__(cls)
            
            try:
                ip_address = cls._instance.get_ip_address()
            except:
                ip_address = Config().hotspot_ip
            
            Debug.LogSeparator(f"Server is running on : {ip_address}:5000")
            
            cls._instance.app = Flask(__name__)
            cls._instance.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
            cls._instance.app.config['SERVER_NAME'] = f'{ip_address}:5000'
            cls._instance.app.config['APPLICATION_ROOT'] = '/'
            cls._instance.app.config['PREFERRED_URL_SCHEME'] = 'http'
            cls._instance.string_updater = StringUpdater()
            cls._instance.is_running = False
            cls._instance.server = None
            
            cls._instance.page_loaded = False
            
            # Removing useless logs
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
            
            # Home page
            @cls._instance.app.route('/')
            def home():
                Debug.prefixActive = False
                with cls._instance.app.app_context():
                    return render_template('index.html')


            # To refresh page 
            @cls._instance.app.route('/stream')
            def stream():
                def generate_stream():
                    while True:
                        with cls._instance.app.app_context():
                            yield f"data: {json.dumps(cls._instance.string_updater.text, ensure_ascii=False)}\n\n"
                            cls._instance.string_updater.update_event.wait()
                            cls._instance.string_updater.update_event.clear()

                return Response(generate_stream(), mimetype='text/event-stream')




            # Check if page has been loaded for client
            # ---------------------------------------------------------------------------- #
            @cls._instance.app.route('/page-loaded', methods=['POST'])
            def page_loaded_event():
                data = request.get_json()
                if data and data.get('loaded'):
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

    def show(self, content):
        
        is_historic = False
        
        for element in content:
            if element["type"] == "standby":
                is_historic = True
        
        if not is_historic:
            self.historic = content
        
        with self.app.app_context():
            for element in content:
                
                transformed_images = []
                # Debug.LogPopup(element)
                if "images" in element:
                    for image in element["images"]:
                        transformed_images.append(url_for('static', filename="images/" + image, _external=True))
                
                    element["images"] = transformed_images
            
            if not self.is_running:
                self.string_updater.show(content)

                self.server = threading.Thread(target=self.app.run, kwargs={'debug': False, 'use_reloader': False})
                self.server.start()
                self.is_running = True
            else:
                self.string_updater.show(content)
                
    def show_historic(self):
        Debug.LogPopup("Show historic", Style.RED)
        
        self.show(self.historic)