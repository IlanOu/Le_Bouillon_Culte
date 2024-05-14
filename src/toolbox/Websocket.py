from src.objects.joystick.StateJoystick import *

import asyncio
import websockets
import json

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None

    async def connection_handler(self, websocket, path):
        try:
            async for message in websocket:
                jsonReceive = json.loads(message)
                match jsonReceive["action"]:
                    case "joystick":
                        if jsonReceive["data"] == "tire":
                            Joystick.set_current_state(StateJoystick.DOWN)
                            print("joystick tirer")
                        else:
                            Joystick.set_current_state(StateJoystick.UP)
                            print("joystick lacher")
                            
                    case _:
                        print("default")
        finally:
            pass

    def start(self):
        start_server = websockets.serve(self.connection_handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        print(f"Serveur WebSocket démarré sur {self.host}:{self.port}")
        asyncio.get_event_loop().run_forever()
    
    def check_action(self):
        pass
""" 
if __name__ == "__main__":
    server = WebSocketServer("0.0.0.0", 8080)
    server.start() """