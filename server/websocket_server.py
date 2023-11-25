import asyncio
import websockets

async def message(websocket, path):
    print(f"Client connected to path: {path}")

    try:
        async for message in websocket:
            print(f"Received message from client: {message}")

            await websocket.send(f"Server received: {message}")

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the client.")

async def main():
    # Start the WebSocket server on localhost, port 8080
    server = await websockets.serve(message, "localhost", 8080)

    print("WebSocket server started on ws://localhost:8080")

    # Keep the server running until it's manually stopped
    await server.wait_closed()

# Run the WebSocket server
asyncio.run(main())
