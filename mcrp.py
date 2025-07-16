import requests
import random
import threading
import time
import argparse

# ============= CONFIGURATION ============= #
NUM_THREADS = 100
URL_TEMPLATE = "https://msrc.microsoft.com/report/vulnerability/VULN-{:06}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B)",
    "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "curl/7.68.0",
    "Wget/1.20.3 (linux-gnu)"
]

HTTP_METHODS = ['GET', 'HEAD']

OUTPUT_FILE = "status_200_reports.txt"

lock = threading.Lock()
PROXIES_LIST = []

# ============= FUNCTIONS ============= #
def random_request():
    num = random.randint(100001, 999999)
    method = random.choice(HTTP_METHODS)
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    url = URL_TEMPLATE.format(num)

    proxy_choice = random.choice(PROXIES_LIST) if PROXIES_LIST else None
    proxies = {"http": proxy_choice, "https": proxy_choice} if proxy_choice else None

    try:
        response = requests.request(method, url, headers=headers, proxies=proxies, timeout=10, allow_redirects=True)
        print(f"[{method}] {url} → {response.status_code}")

        if response.status_code == 200:
            with lock:
                with open(OUTPUT_FILE, "a") as f:
                    f.write(f"{method} {url} → {response.status_code}\n")

    except requests.RequestException as e:
        print(f"[!] {method} {url} ERROR: {e}")

def worker():
    while True:
        random_request()

def main():
    parser = argparse.ArgumentParser(description="MSRC Report ID Enumerator with Proxy Support")
    parser.add_argument("--proxy_list", type=str, help="Path to proxy list text file", required=False)
    args = parser.parse_args()

    global PROXIES_LIST
    if args.proxy_list:
        try:
            with open(args.proxy_list, "r") as f:
                PROXIES_LIST = [line.strip() for line in f if line.strip()]
            print(f"[+] Loaded {len(PROXIES_LIST)} proxies.")
        except Exception as e:
            print(f"[!] Failed to load proxies: {e}")
            return

    print("[*] Starting multithreaded enumeration...")
    threads = []

    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        threads.append(t)

    while True:
        time.sleep(0.1)

if __name__ == "__main__":
    main()
