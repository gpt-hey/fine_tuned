from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import CTransformers
import platform

class TextColor:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

print(TextColor.BLUE + "loaded all libs!" + TextColor.RESET)


# one-time pre-requisite: logging into huggingface
# run the following code adhoc:
# ```
# from huggingface_hub import notebook_login
# notebook_login()
# ```

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

# 3. load pre-trained model
if platform.architecture()[0] == '64bit' and platform.machine() == 'aarch64':
    llm=CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML",
                  model_type="llama",
                  lib="./libctransformers.so",
                  config={'temperature':0.1})
else:
    llm=CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML",
                  model_type="llama",
                  config={'temperature':0.1})


# 4. query using template
template="""Use the following pieces of information to answer the user's question.
If you dont know the answer just say you know, don't try to make up an answer.

Context:{context}
Question:{question}

Only return the helpful answer below and nothing else
Helpful answer
"""

qa_prompt=PromptTemplate(template=template, input_variables=['context', 'question'])
# chain1
chain = RetrievalQA.from_chain_type(llm=llm,
                                   chain_type='stuff',
                                   retriever=vector_store.as_retriever(search_kwargs={'k': 2}),
                                   return_source_documents=True,
                                   chain_type_kwargs={'prompt': qa_prompt})


question="how old is jude and what does he do"
result=chain({'query':question})

print('result: ', result['result'])

