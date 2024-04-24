import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class PyQtWindowThread(QThread):
    finished = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.window = None
        self.app = app

    def run(self):
        # self.app = QApplication(sys.argv)
        self.app.exec_()
        self.finished.emit()

    def open_window(self, text):
        self.window = QWidget()
        self.window.setWindowTitle("Fenêtre PyQt5")
        self.window.showFullScreen()

        label = QLabel(text, self.window)
        label.setAlignment(Qt.AlignCenter)
        label.resize(self.window.size())

        self.window.show()

    def close_window(self):
        if self.window:
            self.window.close()
            self.window = None

# # Exemple d'utilisation
# window_thread = PyQtWindowThread()
# window_thread.start()

# window_thread.open_window("Coucou")
# # ... effectuer des actions ici, par exemple tts.say("Coucou") ...
# window_thread.close_window()