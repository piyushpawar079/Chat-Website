from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.websockets import WebSocket, WebSocketDisconnect
from manager import WebSocketManager

app = FastAPI()

templates = Jinja2Templates(
    directory='templates'
)

manager = WebSocketManager()

@app.get('/')
async def root(request: Request):
    return templates.TemplateResponse(
        request,
        'index.html',
        {}
    )

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    while True:
        try:
            # Used to send message only to itself
            # message = await websocket.receive_json() 
            # print(f"The message received is: {message}")
            # await manager.send_message(message, websocket)
            
            # Use to broadcast the message to all the clients 
            message = await websocket.receive_json()
            print(message)
            for client in manager.connected_clients:
                await manager.send_message(message, client)
        except WebSocketDisconnect:
            await manager.disconnect(websocket)
            break