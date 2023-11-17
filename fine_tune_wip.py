import os
import torchvision
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
from huggingface_hub import notebook_login
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain import HuggingFacePipeline
from langchain.text_splitter import CharacterTextSplitter
import textwrap
import sys
import torch

BASE_LLM_MODEL = "meta-llama/Llama-2-7b-chat-hf"

class TextColor:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

print(TextColor.BLUE + "loaded all libs!" + TextColor.RESET)

# set up hugging face api token
os.environ['HuggingFaceHub_API_Token']= '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'
print(TextColor.BLUE + "set up huggingFace API token!" + TextColor.RESET)

# load and prepare sample training data
loader = UnstructuredFileLoader('./sample.pdf')
documents = loader.load()
text_splitter=CharacterTextSplitter(separator='\n',
                                    chunk_size=1000,
                                    chunk_overlap=50)
text_chunks=text_splitter.split_documents(documents)


# Note: for GPU support use model_kwargs={'device': 'cuda'}
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
vectorstore=FAISS.from_documents(text_chunks, embeddings)

print(TextColor.BLUE + "load and prepare sample training data!" + TextColor.RESET)

# load token from pre-trained model
tokenizer = AutoTokenizer.from_pretrained(BASE_LLM_MODEL)
model = AutoModelForCausalLM.from_pretrained(BASE_LLM_MODEL,
                                             device_map='auto',
                                             torch_dtype=torch.float,
                                             use_auth_token=True,
                                            #  load_in_8bit=True,
                                             load_in_4bit=True
                                            )

print(TextColor.BLUE + "loaded token from pre-trained model!" + TextColor.RESET)

# train on new data
pipe = pipeline("text-generation",
                model=model,
                tokenizer= tokenizer,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                max_new_tokens = 1024,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id
                )
llm=HuggingFacePipeline(pipeline=pipe, model_kwargs={'temperature':0})
chain =  RetrievalQA.from_chain_type(llm=llm, chain_type = "stuff",return_source_documents=True, retriever=vectorstore.as_retriever())
print(TextColor.BLUE + "trained on new data!" + TextColor.RESET)

# query on new trained model
query = "how old is jude and what does he do for living?"
result=chain({"query": query}, return_only_outputs=True)
wrapped_text = textwrap.fill(result['result'], width=500)
wrapped_text