import threading
from websocket_server import WebsocketServer
import json
import time

from src.toolbox.Debug import *

# Définition de la classe du serveur WebSocket
class WebSocketServerThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.server = WebsocketServer(host, port)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)
        self.callback = None
        self.clients_connected = 0

    def run(self):
        self.server.run_forever()

    def new_client(self, client, server):
        self.clients_connected += 1

    def client_left(self, client, server):
        Debug.LogWarning(f"[Websocket]> Client déconnecté : {client['id']}")

    def message_received(self, client, server, message):
        if "{" in message:
            Debug.LogWhisper("[Websocket]> " + message)
            jsonMessage = json.loads(message)
            if jsonMessage["action"] == "checkRFID":
                self.send_message_to_callback(jsonMessage["data"])
            elif jsonMessage["action"] == "RFID":
                self.send_message_to_callback(jsonMessage["data"])
        else:
            pass

    def send_message_to_callback(self, message):
        if self.callback:
            self.callback(message)

    def addCallbackTest(self, callback):
        self.callback = callback

    def addCallbackRun(self, callback):
        self.callback = callback

    def send_message_to_all(self, message):
        if self.clients_connected == 2:
            self.server.send_message_to_all(message)
        else:
            time.sleep(0.3)
            self.send_message_to_all(message)


# if __name__ == "__main__":
#     host = "0.0.0.0"
#     port = 8080
#     server_thread = WebSocketServerThread(host, port)
#     Debug.LogWhisper(f"[Websocket]> Serveur WebSocket démarré sur {host}:{port}")
#     server_thread.start()