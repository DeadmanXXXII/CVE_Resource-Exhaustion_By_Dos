import requests
import random
import string
import concurrent.futures
import argparse
import time

# List of user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
]

BASE_URL = "https://patents.google.com/patent/US{}A"

# Function to generate a random user agent
def random_ua():
    return random.choice(USER_AGENTS)

# Function to build the patent number string (e.g., '0000001')
def format_number(num, length=7):
    return str(num).zfill(length)

# Function to request and process a single patent ID
def check_patent(num, proxies=None, timeout=5):
    formatted_num = format_number(num)
    url = BASE_URL.format(formatted_num)
    headers = {"User-Agent": random_ua()}

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            print(f"[VALID] {url} ✅")
            with open("valid_patents.txt", "a") as f:
                f.write(url + "\n")
        else:
            print(f"[{response.status_code}] {url}")
    except requests.RequestException as e:
        print(f"[ERROR] {url}: {e}")

# Main execution function
def main(start, end, concurrency, proxy_file=None):
    proxies = None

    # Load proxies if provided
    proxy_list = []
    if proxy_file:
        with open(proxy_file) as f:
            proxy_list = [line.strip() for line in f if line.strip()]

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []

        for num in range(start, end + 1):
            # Rotate proxies if provided
            proxy = None
            if proxy_list:
                chosen = random.choice(proxy_list)
                proxy = {"http": chosen, "https": chosen}

            futures.append(executor.submit(check_patent, num, proxy))

        # Wait for all to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PoC for enumerating Google Patents IDs.")
    parser.add_argument("--start", type=int, required=True, help="Start patent number (e.g., 1)")
    parser.add_argument("--end", type=int, required=True, help="End patent number (e.g., 1000000)")
    parser.add_argument("--concurrency", type=int, default=20, help="Number of concurrent threads")
    parser.add_argument("--proxy", type=str, help="Optional proxy list file")

    args = parser.parse_args()

    main(args.start, args.end, args.concurrency, args.proxy)
