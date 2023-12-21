from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import dill as pickle

load_dotenv()

file_path = "faiss_store_openai.pkl"


def fetch_page():
    urls = ["https://stripe.com/docs/treasury/marketing-treasury"]
    loader = UnstructuredURLLoader(urls=urls)
    return loader.load()


def split_text(data):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    return text_splitter.split_documents(data)

def create_embeddings(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(chunks, embeddings)

    with open(file_path, "wb") as f:
        pickle.dump(vectorstore_openai, f)
        

print("Fetching the page")
data = fetch_page()

print("Splitting the content")
chunks = split_text(data)

print("Create Embeddings and store")
create_embeddings(chunks)
