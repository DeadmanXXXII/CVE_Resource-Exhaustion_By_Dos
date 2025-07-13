import requests
import string
import random
import threading

# Base URL
base_url = 'https://www.getglobaloffer.com/'

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A705FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36"
]

# Function to generate six-character combinations
def generate_combinations():
    combinations = []
    for c1 in string.ascii_uppercase:
        for c2 in string.ascii_uppercase:
            for c3 in string.ascii_uppercase:
                for c4 in string.digits:
                    for c5 in string.digits:
                        for c6 in string.digits:
                            combinations.append(f'{c1}{c2}{c3}{c4}{c5}{c6}')
    return combinations

# Function to make HEAD requests
def check_url(prefix, suffix):
    url = f'{base_url}{prefix}/{suffix}'
    headers = {
        'User-Agent': random.choice(user_agents)  # Randomly select a user agent
    }
    try:
        response = requests.head(url, headers=headers, timeout=5)
        print(f'{url} - Status: {response.status_code} - User-Agent: {headers["User-Agent"]}')
    except requests.RequestException as e:
        print(f'{url} - Error: {e} - User-Agent: {headers["User-Agent"]}')

# Function to run the check infinitely
def infinite_loop(prefix_combinations, suffix_combinations):
    while True:
        prefix = random.choice(prefix_combinations)
        suffix = random.choice(suffix_combinations)
        thread = threading.Thread(target=check_url, args=(prefix, suffix))
        thread.start()

if __name__ == "__main__":
    # Generate all combinations for both the prefix and suffix
    prefix_combinations = generate_combinations()
    suffix_combinations = generate_combinations()

    # Start the infinite loop with multithreading
    infinite_loop(prefix_combinations, suffix_combinations)
