# First, we import the necessary modules
import os  # os module for interacting with the operating system
import requests  # requests module for making HTTP requests
import numpy as np  # numpy for scientific computing (not used in this snippet)
from dotenv import load_dotenv  # dotenv for loading environment variables from a .env file

# We load environment variables from a .env file
load_dotenv()

# We get the value of the OKLINK_API_KEY environment variable
api_key = os.getenv('OKLINK_API_KEY')

# We create a dictionary to be used as headers in our HTTP requests
headers = {
    "Ok-Access-Key": api_key,
    "Content-Type": "application/json",
}

# In token_holdings.py
# We define a function to fetch token holdings
def fetch_token_holdings(address, page=1):
    # The URL of the API we're going to call
    url = f"https://www.oklink.com/api/v5/explorer/btc/address-balance-list"
    # The parameters to be included in the URL's query string
    params = {"address": address, "page": page, "limit": 20}
    # We make a GET request to the API
    response = requests.get(url, headers=headers, params=params)
    
    # If the HTTP status code is 200 (OK)
    if response.status_code == 200:
        # We get the response data in JSON format
        data = response.json()
        # If the data includes a 'data' key and a 'balanceList' key in the first item of the 'data' list
        if data and 'data' in data and data['data'] and 'balanceList' in data['data'][0]:
            # We return the 'balanceList'
            return data['data'][0]['balanceList']
        else:
            # If the keys are not found, we print a message and return an empty list
            print(f'No balance data found in response: {data}')
            return []  
    else:
        # If the HTTP status code is not 200, we print the status code and response message, and return an empty list
        print(f'HTTP Status Code: {response.status_code}')
        print(f'Response Message: {response.text}')
        return []

"""
How to add to the code:
This Python code fetches token holdings from an API and returns them. Here are a few ways you could extend it:

- Fetch more data: The API may offer other endpoints with different data. You could add functions to fetch data from these other endpoints.

- Paginate: The fetch_token_holdings function only fetches one page of data. You could modify it to fetch all pages of data.

- Error handling: If the API request fails (e.g., if the API key is invalid), the program will crash. Consider adding error handling to prevent this.

- Caching: If the same address is requested multiple times in a short period, consider caching the result to reduce the load on the API and speed up your program.

Remember, when modifying this code, to keep in mind the API's rate limits and terms of service.
"""
