
import requests
import random
import threading
import time
import csv
from datetime import datetime

# Define a list of random User-Agent strings
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
]

# Generate a random 9-digit suffix to append
def generate_random_url(base_url):
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return base_url[:-9] + random_digits

# Send request and record data
def send_request(url, writer_lock, csv_writer):
    random_url = generate_random_url(url)
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    try:
        start_time = time.time()
        response = requests.get(random_url, headers=headers)
        end_time = time.time()
        duration = round(end_time - start_time, 4)
        with writer_lock:
            csv_writer.writerow([datetime.now().isoformat(), random_url, response.status_code, duration])
        print(f"[{datetime.now().isoformat()}] URL: {random_url} | Status: {response.status_code} | Time: {duration}s")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().isoformat()}] Request failed: {e}")

# Thread runner
def thread_function(base_url, num_requests, writer_lock, csv_writer):
    for _ in range(num_requests):
        send_request(base_url, writer_lock, csv_writer)

if __name__ == "__main__":
    base_urls = [
        "https://www.xvideos.com/profileslist/164356176",
        "https://www.xvideos.com/profileslist/954352176"
    ]
    num_threads = 10
    requests_per_thread = 100

    threads = []
    writer_lock = threading.Lock()

    with open("frontend_stressor_log.csv", "w", newline="") as logfile:
        csv_writer = csv.writer(logfile)
        csv_writer.writerow(["Timestamp", "Requested URL", "Status Code", "Duration"])
        
        for base_url in base_urls:
            for _ in range(num_threads):
                thread = threading.Thread(target=thread_function, args=(base_url, requests_per_thread, writer_lock, csv_writer))
                thread.start()
                threads.append(thread)
        
        for thread in threads:
            thread.join()
