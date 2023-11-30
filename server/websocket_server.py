import asyncio
import websockets
from callbacks import websocket_callback_singleton
from models.llama2_model import llama2_chain
from remindme_parser import Remindme

PORT = 8081

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

            # if none matched before, trigger llm model
            llama2_chain({'query': message})

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the client.")

async def main():
    # Start the WebSocket server on localhost, port 8081
    server = await websockets.serve(message, "localhost", PORT)

    print(f"WebSocket server started on ws://localhost:{PORT}")

    # Keep the server running until it's manually stopped
    await server.wait_closed()

# Run the WebSocket server
asyncio.run(main())
