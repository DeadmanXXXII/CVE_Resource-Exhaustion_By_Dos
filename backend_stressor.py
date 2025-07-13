
import requests
import random
import threading
import time
from datetime import datetime

# List of User-Agent headers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
]

# Generate random 9-digit suffix
def generate_random_url(base_url):
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return base_url[:-9] + random_digits

def send_request(url, log_file):
    random_url = generate_random_url(url)
    headers = {"User-Agent": random.choice(user_agents)}
    try:
        start = time.time()
        response = requests.get(random_url, headers=headers)
        duration = time.time() - start
        log_entry = f"{datetime.now()}, {random_url}, {response.status_code}, {duration:.2f}s\n"
    except requests.exceptions.RequestException as e:
        log_entry = f"{datetime.now()}, {random_url}, FAILED, {str(e)}\n"

    with open(log_file, "a") as f:
        f.write(log_entry)

def thread_function(base_url, num_requests, log_file):
    for _ in range(num_requests):
        send_request(base_url, log_file)

if __name__ == "__main__":
    base_urls = [
        "https://www.xvideos.com/profileslist/164356176",
        "https://www.xvideos.com/profileslist/954352176"
    ]
    num_threads = 20
    requests_per_thread = 50
    log_file = "backend_stress_log.csv"

    threads = []
    for base_url in base_urls:
        for _ in range(num_threads):
            thread = threading.Thread(target=thread_function, args=(base_url, requests_per_thread, log_file))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"Log saved to {log_file}")
