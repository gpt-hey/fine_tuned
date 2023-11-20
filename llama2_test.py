from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextColor:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="./llama-2-7b.gguf.q4_K_M.bin",
    temperature=0.75,
    max_tokens=500,
    top_p=1,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)


# 1. load the notes text data
loader = TextLoader("./sample.txt")
documents=loader.load()

text_splitter=RecursiveCharacterTextSplitter(
                                             chunk_size=500,
                                             chunk_overlap=20)
text_chunks=text_splitter.split_documents(documents)
print(TextColor.BLUE + "load and prepare sample training data!" + TextColor.RESET)

# 2. convert the text chunks into Embeddings and create a FAISS vector store 
embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device':'cpu'})
vector_store=FAISS.from_documents(text_chunks, embeddings)
print(TextColor.BLUE + "convert text chunks into embeddings!" + TextColor.RESET)

template="""Use the following pieces of information to answer the user's question.
If you dont know the answer just say you know, don't try to make up an answer.

Context:{context}
Question:{question}

Only return the helpful answer below and nothing else
Helpful answer
"""

qa_prompt=PromptTemplate(template=template, input_variables=['context', 'question'])
print(TextColor.BLUE + "create q&a template!" + TextColor.RESET)
chain = RetrievalQA.from_chain_type(llm=llm,
                                   chain_type='stuff',
                                   retriever=vector_store.as_retriever(search_kwargs={'k': 2}),
                                   return_source_documents=True,
                                   chain_type_kwargs={'prompt': qa_prompt})

question="how old is jude and what does he do"
result=chain({'query':question})
print(TextColor.GREEN + 'result: ', result['result'] + TextColor.RESET)


# template = """Question: {question}

# Answer: Let's work this out in a step by step way to be sure we have the right answer."""

# prompt = PromptTemplate(template=template, input_variables=["question"])
# prompt = """
# Question: What is AI
# """
# llm(prompt)