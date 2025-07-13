import requests
import random
import string
import time

# Base URL for LinkedIn Help Center
base_url = "https://www.linkedin.com/help/linkedin/answer/a"

# Random User Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
]

def generate_random_url(base):
    # Generate a random 7-character alphanumeric string
    random_chars = ''.join(random.choices(string.digits, k=7))
    return base + random_chars

def send_request(url):
    # Choose a random User Agent
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    response = requests.head(url, headers=headers)
    print(f"Requested URL: {url} | Status Code: {response.status_code}")

# Generate and request random URLs
for _ in range(1000):  # Modify this number to increase/decrease the number of requests
    random_url = generate_random_url(base_url)
    send_request(random_url)
    time.sleep(0.1)  # Pause between requests to simulate more realistic traffic
