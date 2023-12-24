from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from web_scrap import scrape_with_playwright, get_marketing_strings, schema, get_final_result
from dotenv import load_dotenv
import copyreg, ssl

load_dotenv()

def fetch_page(urls):
    print("Fetching using URL Loader:", urls)
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

        

def process_compliance_url(url):
    print("Fetching the compliance page")
    data = fetch_page(urls=url)

    print("Splitting the content")
    chunks = split_text(data)

    print("Create Embeddings and store")
    db = create_embeddings_and_store(chunks)
    return db


def process_url_to_check(url):
    print("Scraping the page to check: ", url)

    extracted_content = scrape_with_playwright(urls=url, schema=schema)
    print("extracted the content")

    strings = get_marketing_strings(extracted_content=extracted_content)
    print("extracted the final set of strings:", strings)

    query = "".join(strings)
    print("final query: ", query)
    return query

def start_processing(urls):
    db = process_compliance_url(url=[urls[0]])
    query = process_url_to_check(url=[urls[1]])
    
    docs = db.similarity_search(query, k=1)
    print("performing semantic search\n", docs)

    result = get_final_result(docs, query)
    print("final result: ", result)
    
    return result