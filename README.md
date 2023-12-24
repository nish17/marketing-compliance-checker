# web-marketing-compliance-checker

## Overview
The Web marketing Compliance Checker is an API designed to assess web content against a specified compliance policy. It takes two URLs as input: one pointing to the compliance policy and another to the web page that needs to be checked. It then returns an assessment of the web content's compliance.

## Features
- **Web Scraping**: Dynamically scrapes content from any given URL.
- **Compliance Checking**: Checks scraped content against specified compliance policies.



## Installation

### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Dependencies
Install the necessary Python packages by running:
```bash
pip install -r requirements.txt
```

### How to run locally?

```sh
# start the server
$ python api.py

# server starts on port 5000
# * Running on http://127.0.0.1:5000 
```

### Architecture

<img width="718" alt="image" src="https://github.com/nish17/marketing-compliance-checker/assets/12984120/3e0570e3-a4db-40db-a7fb-6771f3b6db6e">


There are 2 query params

1. url-to-check
2. compliance-policy

### Example cURL request

```sh

curl --location 'http://127.0.0.1:5000/process_urls?url-to-check=https%3A%2F%2Fwww.joinguava.com%2F&compliance-policy=https%3A%2F%2Fstripe.com%2Fdocs%2Ftreasury%2Fmarketing-treasury'

```

### Learnings

1. promptTemplate
    
    ```python
    prompt = PromptTemplate(
                input_variables=["product"],
                template="What is a good company name that makes {product}?",
            )
    
    prompt.format(product="Smart Apps using Large Language Models (LLMs)")
    ```
    easier, faster and cleaner way to reuse prompt and just change variables

2. Importance of Text splitting, creating embeddings

3. Benefits of semantic search which uses word embedding
    1. store in a vector database for efficient and faster retrieval

## ❤️ Credits

- [Python](https://www.python.org/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)


## 🎓 License

[MIT](LICENSE)
