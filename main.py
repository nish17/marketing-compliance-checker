from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from web_scrap import scrape_with_playwright, get_marketing_strings, schema, get_final_result

from dotenv import load_dotenv
import dill as pickle
import copyreg, ssl

load_dotenv()
file_path = "faiss_store_openai.pkl"

def save_sslcontext(obj):
    return obj.__class__, (obj.protocol,)

copyreg.pickle(ssl.SSLContext, save_sslcontext)
context = ssl.create_default_context()


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

def create_embeddings_and_store(chunks):
    db = FAISS.from_documents(chunks, OpenAIEmbeddings())
    return db

        

print("Fetching the compliance page")
data = fetch_page()

print("Splitting the content")
chunks = split_text(data)

print("Create Embeddings and store")
db = create_embeddings_and_store(chunks)


urls = ["https://www.joinguava.com/"]
print("Scraping the page to check: ", urls)

extracted_content = scrape_with_playwright(urls=urls, schema=schema)
print("extracted the content")

strings = get_marketing_strings(extracted_content=extracted_content)
print("extracted the final set of strings:", strings)

query = "".join(strings)
print("final query: ", query)

# query = strings[0]
# print("query: ", query)
docs = db.similarity_search(query, k=1)
print("performing semantic search\n", docs)
# print(len(docs))

result = get_final_result(docs, query)
print("final result: ", result)