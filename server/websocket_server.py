import asyncio
import websockets
from callbacks import websocket_callback_singleton
from models.llama2_gguf_model import Llama2GGUFModel
from remindme_parser import Remindme

PORT = 8081
ADDRESS = "0.0.0.0"

async def message(websocket, path):
    print(f"Client connected to path: {path}")
    websocket_callback_singleton.set_websocket(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            r = Remindme()
            if r.is_matched(message):
                resp = r.execute_action(message)
                await websocket.send(f'remindme executed: {resp}')
                return

            gguf_model = Llama2GGUFModel()
            if gguf_model.is_matched(message):
                gguf_model.execute_action(message)
                return

            await websocket.send('voided conversation with no match')

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the client.")

async def main():
    async with websockets.serve(message, ADDRESS, PORT):
        print(f"WebSocket server started on ws://{ADDRESS}:{PORT}")
        await asyncio.Event().wait()


# Run the WebSocket server
asyncio.run(main())
