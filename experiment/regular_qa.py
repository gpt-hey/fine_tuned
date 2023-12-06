from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import CTransformers
import platform
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class CustomStreamingCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
    def on_llm_new_token(self, token, **kwargs):
        """Run on new LLM token. Only available when streaming is enabled."""
        self.queue.append(token)



queue = []
# 3. load pre-trained model
if platform.architecture()[0] == '64bit' and platform.machine() == 'aarch64':
    llm=CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML",
                  model_type="llama",
                  lib="./libctransformers.so",
                  stream=True,
                  callbacks=[CustomStreamingCallbackHandler(queue), StreamingStdOutCallbackHandler()],
                  config={'temperature':0.1})
else:
    llm=CTransformers(model="TheBloke/Llama-2-7B-Chat-GGML",
                  model_type="llama",
                  stream=True,
                  callbacks=[CustomStreamingCallbackHandler(queue), StreamingStdOutCallbackHandler()],
                  config={'temperature':0.1})

# regular Q&A chain
regular_qa_prompt = PromptTemplate(
    input_variables=["question"],
    template="""The following is a friendly conversation between a human and an AI with human asking a lot of questions. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
    Current conversation: {history}
    Human: {question}
    AI:""",
)

# 1. flush (without template) 
llm("tell me a joke")
for token in queue:
    print('bare bone: ', token)

# 2. flush (with template + empty history)
chain = LLMChain(llm=llm, prompt=regular_qa_prompt)
res = chain({"question": "what's your name?", "history": ""})
for token in queue:
    print('with template: ', token)

