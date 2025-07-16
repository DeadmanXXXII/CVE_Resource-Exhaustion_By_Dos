import requests
import random
import threading
import time
import argparse
import os
from datetime import datetime

# ============= CONFIGURATION ============= #
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

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'OPTIONS']

OUTPUT_FILE = "status_200_reports.txt"
lock = threading.Lock()
PROXIES_LIST = []

# Ensure responses directory exists if needed
os.makedirs("responses", exist_ok=True)

def random_request(args):
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

        status_line = f"[{method}] {url} → {response.status_code} ({response.url})"
        headers_str = f"Headers: {dict(response.headers)}"
        timestamp_str = f"[{datetime.utcnow().isoformat()}]" if args.timestamp else ""

        log_entry = f"{timestamp_str} {status_line}\n{headers_str}\n\n"

        print(status_line)
        print(headers_str)

        with lock:
            # Write to main log file
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)

            # Save body and/or split files if requested
            if args.save_body or args.split_files:
                filename_base = f"responses/{method}_{num}"
                if args.split_files:
                    with open(f"{filename_base}.txt", "w", encoding="utf-8") as f:
                        f.write(log_entry)
                        if args.save_body:
                            f.write("\n=== BODY START ===\n")
                            f.write(response.text)
                            f.write("\n=== BODY END ===\n")
                elif args.save_body:
                    with open(f"{filename_base}.body.html", "w", encoding="utf-8") as f:
                        f.write(response.text)

    except requests.RequestException as e:
        error_line = f"[!] {method} {url} ERROR: {e}\n"
        print(error_line)
        with lock:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(error_line)

def worker(args):
    while True:
        random_request(args)

def main():
    parser = argparse.ArgumentParser(description="MSRC Report Enumerator with advanced features")
    parser.add_argument("--proxy_list", type=str, help="Path to proxy list text file", required=False)
    parser.add_argument("--threads", type=int, default=100, help="Number of threads to run")
    parser.add_argument("--save_body", action="store_true", help="Save full HTML response body")
    parser.add_argument("--split_files", action="store_true", help="Write each request result into its own file")
    parser.add_argument("--timestamp", action="store_true", help="Include UTC timestamps in log entries")
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

    print(f"[*] Starting with {args.threads} threads...")

    threads = []
    for _ in range(args.threads):
        t = threading.Thread(target=worker, args=(args,), daemon=True)
        t.start()
        threads.append(t)

    while True:
        time.sleep(0.1)

if __name__ == "__main__":
    main()
