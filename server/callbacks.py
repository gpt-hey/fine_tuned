from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
class WebsocketCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self, websocket):
        self.websocket = websocket
    async def on_llm_new_token(self, token, **kwargs):
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.websocket.send(token)