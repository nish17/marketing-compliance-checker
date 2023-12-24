import dotenv
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import (
    PromptTemplate,
)
from langchain.chains import create_extraction_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

dotenv.load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

important_html_tags = [
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "a",
    "img",
    "ul",
    "ol",
    "li",
    "strong",
    "em",
    "blockquote",
    "button",
    "title",
    "form"
]


schema = {
    "properties": {
        "pageTitle": {
            "type": "string"
        },
        "promotionalFeatures": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string"
                    }
                }
            }
        },
        "keyHighlights": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "highlight": {
                        "type": "string"
                    }
                }
            }
        },
    },
    "required": ["pageTitle", "promotionalFeatures", "keyHighlights"]
}


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    print('Fetching...')
    # print(docs)
    print('Transforming...')
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=important_html_tags
    )
    print("Docs transformed:")
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    return extracted_content

def get_marketing_strings(extracted_content):
    prompt = PromptTemplate(
        template="From the following json object, please return a list of strings which are promotional/marketing type content messages.\n\n{extracted_content}\n",
        input_variables=["extracted_content"],
    )

    _input = prompt.format_prompt(extracted_content=extracted_content)

    model = OpenAI(temperature=0)
    output = model(_input.to_string())
    return output

def get_final_result(rules, strings):
    prompt = PromptTemplate(
        template="Assume you are an marketing compliance expert. Please check if the following strings \n\n ```{strings}```\n\n Are complaint enough with thee following policy\n\n```{rules}```\n\n In the final output please only give the final result of strings which are non-compliant with the policy in a json format",
        input_variables=["rules", "strings"]
    )
    
    _input = prompt.format(rules=rules, strings=strings)
    model = OpenAI(temperature=0)
    output = model(_input)
    return output
