# spice/__init__.py
# We start by importing the necessary modules
from flask import Flask, jsonify, request, render_template  # flask modules for web server and request handling
from .brc20_wallet_tokens import fetch_address_tokens_sync  # our own module to fetch token data
from .token_holdings import fetch_token_holdings  # our own module to fetch token holdings
from .transaction_history import fetch_transactions_sync

# We create an instance of the Flask class
app = Flask(__name__)

# We define a route for the root URL ("/")
@app.route('/')
def index():
    # When this route is hit, we render the index.html template
    return render_template('index.html')

# We define another route for "/api/fetch_data" where we expect GET requests
@app.route('/api/fetch_data', methods=['GET'])
def fetch_data():
    # We get the 'address' parameter from the request's query string, or use a default value if it's not provided
    address = request.args.get('address', default='bc1p2xmduzppdyw05xj9zk2v0fqwwhga84kvnzg3fue27646rmqlverqd9lxf6')
    # We use the address to fetch token data
    data = fetch_address_tokens_sync(address)
    # We return the data as JSON
    return jsonify(data)

# We define another route for "/api/fetch_chart_data"
@app.route("/api/fetch_chart_data")
def fetch_chart_data():
    # We get the 'address' parameter from the request's query string, or use a default value if it's not provided
    address = request.args.get("address", default='bc1p2xmduzppdyw05xj9zk2v0fqwwhga84kvnzg3fue27646rmqlverqd9lxf6')
    # If no address is provided, we return an error
    if not address:
        return jsonify({"error": "No address provided"}), 400
    # If an address is provided, we fetch the token holdings for that address
    data = fetch_token_holdings(address)
    # We return the token holdings as JSON
    return jsonify(data)

@app.route('/api/fetch_transaction_history', methods=['GET'])
def fetch_transaction_history():
    address = request.args.get('address')
    page = int(request.args.get('page', 1))
    data, total_count = fetch_transactions_sync(address, page)
    return jsonify({
        'total_count': total_count,
        'transactions': data
    })


"""
How to add to the code:
This Python code handles web requests and uses data fetched from the blockchain to provide responses. 
Here are a few ways you could extend it:

- Add more endpoints: Right now, there are only two endpoints ("/" and "/api/fetch_data"). You could add more endpoints to handle more types of requests.

- Improve error handling: If the functions fetch_address_tokens_sync or fetch_token_holdings encounter an error, the server could crash. Consider adding error handling in these functions to prevent this.

- Add more data in the responses: The responses currently include only the bare minimum of data. You could modify the fetch_address_tokens_sync and fetch_token_holdings functions to fetch and return more information.

- Optimize for performance: If the blockchain data fetching is slow, it could cause the web server to hang. Consider ways to fetch the data more efficiently or to cache it so that it doesn't need to be fetched for each request.

Remember, when modifying this code, consider both the web server and the data fetching logic. Changing one may require changes in the other.
"""
