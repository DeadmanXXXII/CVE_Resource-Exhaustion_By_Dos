import itertools
import string
import requests
import random
import time

# List of base URLs
base_urls = [
    "https://app.intigriti.com/researcher/inbox/submissions/d0ff1339-f0c4-4733-a648-1b06b79125e6/ROBINHOOD-",
    "https://app.intigriti.com/researcher/inbox/submissions/2e52d6d3-da18-467f-836e-7a22b82bef5f/TOMORROWLAND-",
    "https://app.intigriti.com/researcher/inbox/submissions/23f5d877-7948-4740-830c-393e66753fc4/MONZOBANK-",
    "https://app.intigriti.com/researcher/inbox/submissions/0083a5bf-e54f-4f79-a972-12a795272c8b/INNOVAPOST-",
    "https://app.intigriti.com/researcher/inbox/submissions/b084e962-1d83-4bec-9d46-0f02c0f7bf88/INNOGAMES-",
]

# List of common user agents
user_agents = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/92.0.4515.131 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    # Safari on macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)"
    " Version/14.1.2 Safari/605.1.15",
    # Edge on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
    # Chrome on Android
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/92.0.4515.115 Mobile Safari/537.36",
    # Safari on iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"
    " (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
]

# Characters used for generating variations
characters = string.ascii_uppercase + string.digits

# Function to generate a limited number of random 8-character variations
def generate_random_variations(count):
    for _ in range(count):
        variation = ''.join(random.choices(characters, k=8))
        yield variation

# Function to make requests with rotating user agents and base URLs
def request_variations(base_urls, user_agents, total_requests=1000, delay_between_requests=1):
    base_url_cycle = itertools.cycle(base_urls)
    user_agent_cycle = itertools.cycle(user_agents)

    for variation in generate_random_variations(total_requests):
        base_url = next(base_url_cycle)
        user_agent = next(user_agent_cycle)
        url = base_url + variation
        headers = {'User-Agent': user_agent}

        try:
            response = requests.get(url, headers=headers)
            print(f"Requested URL: {url}, Status Code: {response.status_code}, User-Agent: {user_agent}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for URL: {url}, Error: {e}")

        # Delay between requests to prevent overwhelming the server
        time.sleep(delay_between_requests)

# Parameters
TOTAL_REQUESTS = 10000000000  # Total number of requests to make
DELAY_BETWEEN_REQUESTS = 0.01  # Seconds between each request

# Start making requests
request_variations(base_urls, user_agents, TOTAL_REQUESTS, DELAY_BETWEEN_REQUESTS)
