from fastapi.websockets import WebSocket

class WebSocketManager:

    def __init__(self):
        self.connected_clients = []

    async def connect(self, websocket: WebSocket):
        
        self.client_ip = f"{websocket.client.host}: {websocket.client.port}"
        
        await websocket.accept()
        print(f"client {self.client_ip}")
        
        self.connected_clients.append(websocket)
        print(f"connected clients: {self.connected_clients}")
    
    def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)
        print(f"client {self.client_ip}, disconnected")
        print(f'connected clients: {self.connected_clients}')

    async def send_message(self, message: dict, websocket: WebSocket):
        message = {
            "client": message['username'],
            "message": message['content']
        }

        await websocket.send_json(message)