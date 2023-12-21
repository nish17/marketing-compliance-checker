from langchain.chains import create_extraction_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import UnstructuredURLLoader

from dotenv import load_dotenv
load_dotenv()

def fetch_page():
    print("Fetching snimesh.com")
    urls = ["https://www.snimesh.com/"]
    loader = UnstructuredURLLoader(urls=urls, mode="elements")
    return loader.load()


# Schema
schema = {
    "properties": {
        "marketing_content_title": {"type": "string"},
        "marketing_content_description": {"type": "string"},
        "marketing_content_targeted_to": {"type": "string"},
        "marketing_content_other_important_info": {"type": "string"},
    },
    "required": ["marketing_content_title", "marketing_content_description"],
}
model="gpt-3.5-turbo"
page_content = fetch_page()

print(page_content)

print("====\n\ndone fetching\ncalling gpt-3.5-turbo and creating extraction chain\n")

# llm = ChatOpenAI(temperature=0, model=model)
# chain = create_extraction_chain(schema, llm)

# print(chain.run(page_content))