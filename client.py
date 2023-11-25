import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:8081"  # Replace with the actual WebSocket server URI

    async with websockets.connect(uri) as websocket:
        message = "who is Jude!"
        print(f"Sending message to server: {message}")
        await websocket.send(message)

        response = await websocket.recv()
        print(f"Received response from server: {response}")

# Run the WebSocket client
asyncio.run(send_message())