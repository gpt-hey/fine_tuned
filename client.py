import asyncio
import websockets

async def send_message():
    uri = "ws://0.0.0.0:8081"  # Replace with the actual WebSocket server URI
    # uri = "ws://129.213.151.7:8081"

    async with websockets.connect(uri, ping_timeout=None) as websocket:
        # Send your actual message
        message = "@gguf tell me about yourself"
        print(f"Sending message to server: {message}")
        await websocket.send(message)

        while True:
            try:
                # Receive and print the response from the server
                response = await websocket.recv()
                print(f"Received response from server: {response}")
                if not response:
                    break
            except websockets.exceptions.ConnectionClosed as e:
                print(f"Connection closed by the client. Reason: {e.reason}")
                break
            except asyncio.TimeoutError:
                print("Timeout waiting for response. Closing connection.")
                break
            except Exception as e:
                print(f"An exception occurred: {e}")
                break

# Run the WebSocket client
asyncio.run(send_message())