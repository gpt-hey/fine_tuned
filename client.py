import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:8081"  # Replace with the actual WebSocket server URI

    async with websockets.connect(uri) as websocket:
        message = "@remindme to take notes!"
        # message = "tell me about yourself"
        print(f"Sending message to server: {message}")
        await websocket.send(message)
        while True:
            try:
                response = await websocket.recv()
                print(f"Received response from server: {response}")
                if not response:
                    break
            except Exception as e:
                print(f"An exception occurred: {e}")
                break

# Run the WebSocket client
asyncio.run(send_message())
# asyncio.get_event_loop().run_until_complete(send_message())