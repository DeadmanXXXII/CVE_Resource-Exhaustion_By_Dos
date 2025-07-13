import requests
import time

def fetch_headers(i):
    url = f"https://www.hckrt.com/Reports/Details/{i:03}"
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        print(f"\n[+] {url} -> {response.status_code}")
        print("-" * 60)
        for k, v in response.headers.items():
            print(f"{k}: {v}")
    except requests.exceptions.RequestException as e:
        print(f"[-] {url} -> ERROR: {e}")

# Infinite loop: 000 to 656 repeatedly
while True:
    for i in range(657):
        fetch_headers(i)
        time.sleep(0.25)  # Optional: throttle slightly to avoid immediate detection
