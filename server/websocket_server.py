import asyncio
import websockets
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from text_loader import load_content
from text_color import TextColor
from qa_template import TEMPLATE

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="../llama-2-7b.gguf.q4_K_M.bin",
    temperature=0.75,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)
text_chunks = load_content()
embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device':'cpu'})
vector_store=FAISS.from_documents(text_chunks, embeddings)
print(TextColor.BLUE + "convert text chunks into embeddings!" + TextColor.RESET)

# create chain
qa_prompt=PromptTemplate(template=TEMPLATE, input_variables=['context', 'question'])
print(TextColor.BLUE + "create q&a template!" + TextColor.RESET)
chain = RetrievalQA.from_chain_type(llm=llm,
                                   chain_type='stuff',
                                   retriever=vector_store.as_retriever(search_kwargs={'k': 2}),
                                   return_source_documents=True,
                                   chain_type_kwargs={'prompt': qa_prompt})

async def message(websocket, path):
    print(f"Client connected to path: {path}")

    try:
        async for message in websocket:
            print(f"Received message from client: {message}")
            result=chain({'query': message})
            print(f"llama2 computes result: {result}")
            await websocket.send(f"{result['result']}")

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by the client.")

async def main():
    # Start the WebSocket server on localhost, port 8080
    server = await websockets.serve(message, "localhost", 8081)

    print("WebSocket server started on ws://localhost:8081")

    # Keep the server running until it's manually stopped
    await server.wait_closed()

# Run the WebSocket server
asyncio.run(main())
