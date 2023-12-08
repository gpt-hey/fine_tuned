import asyncio
import websockets
from callbacks import WebsocketCallbackHandler
from models.llama2_gguf_model import Llama2GGUFModel
from remindme_parser import Remindme

PORT = 8081
ADDRESS = "0.0.0.0"

async def handle_websocket_close(websocket):
    try:
        await websocket.close()

    except websockets.exceptions.ConnectionClosedOK:
        # Handle the case where the connection is already closed
        pass
    except Exception as e:
        # Handle other exceptions as needed
        print(f"Error: {e}")

async def message(websocket, path):
    print(f"Client connected to path: {path}")
    callback = WebsocketCallbackHandler(websocket)
    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            r = Remindme()
            if r.is_matched(message):
                resp = await asyncio.to_thread(r.execute_action, message)
                await websocket.send(f'remindme executed: {resp}')
                return

            gguf_model = Llama2GGUFModel(callback)
            if gguf_model.is_matched(message):
                await asyncio.to_thread(gguf_model.execute_action, message)
                return

            await websocket.send('voided conversation with no match')

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the client.")
    finally:
        await handle_websocket_close(websocket)

async def main():
    async with websockets.serve(message, ADDRESS, PORT):
        await asyncio.Future()
        print(f"WebSocket server started on ws://{ADDRESS}:{PORT}")

# Run the WebSocket server
if __name__ == "__main__":
    asyncio.run(main())
