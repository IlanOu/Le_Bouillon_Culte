import threading
from websocket_server import WebsocketServer
import time

# Définition de la classe du serveur WebSocket
class WebSocketServerThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.server = WebsocketServer(host, port)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

    def run(self):
        self.server.run_forever()

    def new_client(self, client, server):
        print(f"Nouveau client connecté : {client['id']}")

    def client_left(self, client, server):
        print(f"Client déconnecté : {client['id']}")

    def message_received(self, client, server, message):
        print(f"Message reçu de {client['id']} : {message}")
        server.send_message_to_all(f"Client {client['id']} a dit : {message}")

# Création et démarrage du serveur WebSocket
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8080
    server_thread = WebSocketServerThread(host, port)
    print(f"Serveur WebSocket démarré sur {host}:{port}")
    server_thread.start()