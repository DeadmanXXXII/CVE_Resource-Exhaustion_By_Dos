import itertools
import string
import requests
import random
import time

# Base URL for raw content on GitHub
base_url = "https://raw.githubusercontent.com/{user}/{repo}/{branch}/README.md"

# List of common user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
    "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
]

# Characters used for generating variations
characters = string.ascii_uppercase + string.digits

# Function to generate a limited number of random 8-character variations
def generate_random_variations(count):
    for _ in range(count):
        variation = ''.join(random.choices(characters, k=8))
        yield variation

# Function to make requests with rotating user agents and base URLs
def request_variations(base_url, user_agents, total_requests=2000000000000000000000000, delay_between_requests=0.001):
    user_agent_cycle = itertools.cycle(user_agents)

    for variation in generate_random_variations(total_requests):
        url = base_url.format(user=variation, repo=variation, branch=variation)
        user_agent = next(user_agent_cycle)
        headers = {'User-Agent': user_agent}

        try:
            response = requests.get(url, headers=headers)
            print(f"Requested URL: {url}, Status Code: {response.status_code}, User-Agent: {user_agent}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for URL: {url}, Error: {e}")

        # Delay between requests to prevent overwhelming the server
        time.sleep(delay_between_requests)

# Start making requests
request_variations(base_url, user_agents)
