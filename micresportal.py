import requests
import random
import threading
import time

# Configuration
NUM_THREADS = 100
URL_TEMPLATE = "https://msrc.microsoft.com/report/vulnerability/VULN-{:06}"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
    "curl/7.68.0",
    "Wget/1.20.3 (linux-gnu)"
]

HTTP_METHODS = ['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']

def random_request():
    num = random.randint(100001, 999999)
    method = random.choice(HTTP_METHODS)
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    url = URL_TEMPLATE.format(num)

    try:
        response = requests.request(method, url, headers=headers, timeout=10, allow_redirects=True)
        print(f"[{method}] {url} → {response.status_code} ({response.url})")
        print(f"Headers: {dict(response.headers)}\n")
    except requests.RequestException as e:
        print(f"[!] {method} {url} ERROR: {e}")

def worker():
    while True:
        random_request()
        # time.sleep(0.1)  # Optional throttle

def main():
    print("[*] Starting random method/URL resource test...")
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    # Run indefinitely
    while True:
        time.sleep(0.1)

if __name__ == "__main__":
    main()
