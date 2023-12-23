from flask import Flask, request, jsonify
from urllib.parse import urlparse

import requests

from main import start_processing

app = Flask(__name__)

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except:
        return False

@app.route('/process_urls', methods=['GET'])
def process_urls():
    # Extracting the URLs from the query parameters
    url1 = request.args.get('compliance-policy')
    url2 = request.args.get('url-to-check')

    # Validating URLs
    if not all([url1, url2]) or not all([is_valid_url(url1), is_valid_url(url2)]):
        return jsonify(error="Invalid or missing URLs"), 400

    # Call your LLM function with the URLs
    result = start_processing(urls=[url1, url2])

    # Return the result as JSON
    return result

if __name__ == '__main__':
    app.run(debug=True) 