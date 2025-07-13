import requests
import random
import threading

# Base URL
base_url = 'https://8ballpool.com/en/?UniqueID='

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A705FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36"
]

# Function to generate a 10-digit number
def generate_unique_id():
    return ''.join(random.choices('0123456789', k=10))

# Function to make GET requests
def check_url(unique_id):
    url = f'{base_url}{unique_id}'
    headers = {
        'User-Agent': random.choice(user_agents)  # Randomly select a user agent
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)  # GET request instead of HEAD
        print(f'{url} - Status: {response.status_code} - User-Agent: {headers["User-Agent"]}')
    except requests.RequestException as e:
        print(f'{url} - Error: {e} - User-Agent: {headers["User-Agent"]}')

# Function to run the check infinitely
def infinite_loop():
    while True:
        unique_id = generate_unique_id()
        thread = threading.Thread(target=check_url, args=(unique_id,))
        thread.start()

if __name__ == "__main__":
    # Start the infinite loop with multithreading
    infinite_loop()
