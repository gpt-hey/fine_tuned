from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from text_loader import load_content
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from text_color import TextColor
from qa_template import TEMPLATE


class Llama2GGUFModel:
    def __init__(self):
        # TODO refactor __init__ and swap out callbackManager to make  init model faster
        self.callback_manager = CallbackManager([])
        self.llm = LlamaCpp(
            model_path="./server/models/llama-2-7b.gguf.q4_K_M.bin",
            temperature=0.7,
            repeat_penalty=1.176,
            top_p=0.1,
            max_tokens=-1,
            callback_manager=self.callback_manager,
            verbose=False,
        )
        text_chunks = load_content()
        embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device':'cpu'})
        self.vector_store=FAISS.from_documents(text_chunks, embeddings)
        print(TextColor.BLUE + "convert text chunks into embeddings!" + TextColor.RESET)

        # create chain
        self.qa_prompt=PromptTemplate(template=TEMPLATE, input_variables=['context', 'question'])
        print(TextColor.BLUE + "create q&a template!" + TextColor.RESET)
    def update_callback_handler(self, callback_handler):
        self.callback_manager.set_handler(callback_handler)
    def is_matched(self, text):
        return "@gguf" in text.lower()
    def execute_action(self, text):
        text = text.replace("@gguf", "")
        llama2_chain = RetrievalQA.from_chain_type(llm=self.llm,
                                   chain_type='stuff',
                                   retriever=self.vector_store.as_retriever(search_kwargs={'k': 2}),
                                   return_source_documents=True,
                                   chain_type_kwargs={'prompt': self.qa_prompt})
        llama2_chain({'query': text})