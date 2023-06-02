import asyncio  # Import asyncio for asynchronous operations
import os  # Import os for accessing environment variables
from tenacity import retry, stop_after_attempt, wait_exponential  # Import retry logic
from ratelimiter import RateLimiter  # Import RateLimiter for rate limiting
import requests  # Import requests for making HTTP requests
from dotenv import load_dotenv  # Import load_dotenv for loading environment variables from a .env file

load_dotenv()  # Load environment variables

api_key = os.getenv('OKLINK_API_KEY')  # Get the API key from environment variables

headers = {  # Headers for the HTTP request
    "Ok-Access-Key": api_key,
    "Content-Type": "application/json",
}

limit = 20  # Define the limit for number of results per page
url = "https://www.oklink.com/api/v5/explorer/btc/address-balance-list"  # The API endpoint

rate_limiter = RateLimiter(max_calls=5, period=1)  # Define the rate limiter

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
# The retry decorator will attempt to re-execute the function if it fails, with exponential backoff
async def fetch_address_tokens(address, page):
    with rate_limiter:  # Use the rate limiter to limit the rate of calls
        params = {"address": address, "page": page, "limit": limit}  # Parameters for the HTTP request
        response = requests.get(url, headers=headers, params=params)  # Make the HTTP request

        if response.status_code == 200:  # If the request was successful
            return response.json()  # Return the response as JSON
        else:  # If the request failed
            print(f'HTTP Status Code: {response.status_code}')
            print(f'Response Message: {response.text}')
            return None  # Return None

async def parallel_fetch(address):  # Fetch all pages in parallel
    all_results = []
    initial_result = await fetch_address_tokens(address, 1)  # Fetch the first page
    total_pages = int(initial_result['data'][0]['totalPage']) if initial_result and 'data' in initial_result and initial_result['data'] else 0
    all_results.append(initial_result)

    if total_pages > 1:  # If there are more than one page
        tasks = [asyncio.ensure_future(fetch_address_tokens(address, i)) for i in range(2, total_pages + 1)]  # Create a task for each page
        results = await asyncio.gather(*tasks, return_exceptions=True)  # Gather the results from all tasks

        for result in results:  # For each result
            if isinstance(result, Exception):  # If the result is an exception
                print(f"Exception occurred: {result}")
                continue  # Skip to the next result

            if 'data' not in result or not isinstance(result['data'], list) or len(result['data']) == 0 or 'balanceList' not in result['data'][0]:
                print(f"Unexpected result: {result}")
                continue  # Skip to the next result

            all_results.append(result)  # Add the result to all_results

    return all_results

def clean_data(fetched_data):  # Clean the fetched data
    cleaned_data = []
    if fetched_data is not None:
        for page_data in fetched_data:
            if 'data' in page_data and isinstance(page_data['data'], list) and len(page_data['data']) > 0 and 'balanceList' in page_data['data'][0]:
                balance_list = page_data['data'][0]['balanceList']
                cleaned_data.extend(balance_list)
    return cleaned_data

def fetch_address_tokens_sync(address):  # Fetch all tokens for a given address
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)  # Set the event loop
    try:
        result = loop.run_until_complete(parallel_fetch(address))  # Run the parallel_fetch function until it completes
        cleaned_data = clean_data(result)  # Clean the result
        return cleaned_data  # Return the cleaned data
    finally:
        loop.close()  # Close the event loop


'''
How to add to the code:

This Python script is responsible for fetching token balances for a given Bitcoin address. Here are a few ways you could extend it:

Add more information: This script currently fetches token balances. You could extend it to fetch more information, such as transaction history or token metadata.

Improve error handling: Currently, if a request fails, the script prints an error message and moves on. You could add more robust error handling, for example by retrying failed requests or by using a fallback API if one is available.

Support more APIs: This script currently fetches data from the OKLink API. You could modify it to fetch data from other APIs as well, and provide a unified interface to the rest of your application.

Add tests: Tests can help ensure your code works as expected, and makes it easier to add new features or refactor existing code.


'''