from langchain.document_loaders import TextLoader
from text_color import TextColor
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_content():
    loader = TextLoader("./sample.txt")
    documents=loader.load()

    text_splitter=RecursiveCharacterTextSplitter(
                                                chunk_size=500,
                                                chunk_overlap=20)
    text_chunks=text_splitter.split_documents(documents)
    print(TextColor.BLUE + "load and prepare sample training data!" + TextColor.RESET)
    return text_chunks