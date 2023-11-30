from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
class WebsocketCallbackHandler(StreamingStdOutCallbackHandler):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebsocketCallbackHandler, cls).__new__(cls)
            # Initialize the singleton instance here
        return cls._instance

    def set_websocket(self, websocket):
        self.websocket = websocket
    async def on_llm_new_token(self, token, **kwargs):
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.websocket.send(token)

websocket_callback_singleton = WebsocketCallbackHandler()