from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import CTransformers
import platform

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
    
print(llm('AI is going to'))

# regular Q&A chain
regular_qa_prompt = PromptTemplate(
    input_variables=["question"],
    template="""The following is a friendly conversation between a human and an AI with human asking a lot of questions. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    Current conversation: {history}
    Human: {question}
    AI:""",
)

chain = LLMChain(llm=llm, prompt=regular_qa_prompt)
result = chain({"question": "what's your name?", "history": ""})
print('result: ', result['text'])