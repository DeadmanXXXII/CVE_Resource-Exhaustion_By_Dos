import random
import string
import requests
import threading

# Function to generate a random 15-digit number as a string
def generate_random_15_digit_number():
    return ''.join(random.choices(string.digits, k=15))

# List of 10 random User Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59"
]

# Base URL parts
base_url_post = "https://www.facebook.com/864455789052895/posts/"
base_url_page = "https://www.facebook.com/"

# Number of requests to generate
#num_requests = 10

# Function to generate random URLs and make requests
def make_request():
    # Choose a random User Agent
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    
    # Generate random number for post URL
    random_number_post = generate_random_15_digit_number()
    new_url_post = base_url_post + random_number_post
    print(f"Generated URL for post: {new_url_post}")

    # Make a GET request to the generated post URL
    try:
        response_post = requests.get(new_url_post, headers=headers)
        print(f"Response code for {new_url_post}: {response_post.status_code}")
    except requests.RequestException as e:
        print(f"Request failed for {new_url_post}: {e}")

    # Generate random number for page URL
    random_number_page = generate_random_15_digit_number()
    new_url_page = base_url_page + random_number_page
    print(f"Generated URL for page: {new_url_page}")

    # Make a GET request to the generated page URL
    try:
        response_page = requests.get(new_url_page, headers=headers)
        print(f"Response code for {new_url_page}: {response_page.status_code}")
    except requests.RequestException as e:
        print(f"Request failed for {new_url_page}: {e}")

# Creating threads for concurrent requests
threads = []
for i in range(num_requests):
    thread = threading.Thread(target=make_request)
    threads.append(thread)
    thread.start()

# Waiting for all threads to complete
for thread in threads:
    thread.join()
