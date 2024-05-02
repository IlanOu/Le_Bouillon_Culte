from flask import Flask, render_template, Response
import time
import threading



class StringUpdater:
    def __init__(self, update_interval=5):
        self.question = "..."
        self.answer = "."
        self.update_interval = update_interval

    def write(self, question="...", answer="."):
        self.question = question
        self.answer = answer

    def start_updater(self):
        thread = threading.Thread(target=self._update_and_stream)
        thread.daemon = True
        thread.start()

    def _update_and_stream(self):
        while True:
            time.sleep(self.update_interval)


class WebApp:
    def __init__(self, string_updater):
        self.app = Flask(__name__)
        self.string_updater = string_updater

    def run(self):
        @self.app.route('/')
        def home():
            return render_template('index.html', string=self.string_updater.question)

        @self.app.route('/stream')
        def stream():
            def generate_stream():
                while True:
                    yield f"data: {self.string_updater.question} ~*-*~ {self.string_updater.answer}\n\n"
                    time.sleep(self.string_updater.update_interval)
            return Response(generate_stream(), mimetype='text/event-stream')

        self.app.run(debug=False)



"""

# Exemple d'utilisation
# ---------------------------------------------------------------------------- #

# Initialisation et exécution de l'application
string_updater = StringUpdater(update_interval=1)
web_app = WebApp(string_updater)

# Démarrer le thread de mise à jour avant d'exécuter l'application
# string_updater.start_updater()
web_app.run()

"""