import asyncio
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from ratelimiter import RateLimiter
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OKLINK_API_KEY')

headers = {
    "Ok-Access-Key": api_key,
    "Content-Type": "application/json",
}

rate_limiter = RateLimiter(max_calls=5, period=1)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def fetch_transactions(address, page=1):
    with rate_limiter:
        url = f"https://www.oklink.com/api/v5/explorer/btc/transaction-list"
        params = {"address": address, "page": page, "limit": 10}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, dict) and 'data' in response_data:
                return response_data
            else:
                print(f"Unexpected response structure: {response_data}")
                return None
        else:
            print(f'HTTP Status Code: {response.status_code}')
            print(f'Response Message: {response.text}')
            return None

def clean_transaction_data(fetched_data):
    cleaned_data = []
    if fetched_data is not None and isinstance(fetched_data, dict):
        if 'data' in fetched_data and isinstance(fetched_data['data'], list) and len(fetched_data['data']) > 0 and 'inscriptionsList' in fetched_data['data'][0]:
            transactions_list = fetched_data['data'][0]['inscriptionsList']
            cleaned_data.extend(transactions_list)
    return cleaned_data

def fetch_transactions_sync(address, page=1, items_per_page=10):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(fetch_transactions(address, page))
        if isinstance(result, dict):
            cleaned_data = clean_transaction_data(result)
            start = (page - 1) * items_per_page
            end = start + items_per_page
            print(cleaned_data[start:end], len(cleaned_data))
            return cleaned_data[start:end], len(cleaned_data)
        else:
            print(f"Error: {result}")
            return [], 0
    finally:
        loop.close()
