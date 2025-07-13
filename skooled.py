import requests
import threading
import random
import time

# List of base URLs to test
base_urls = [
    "https://www.academia.edu/10",
    "https://www.academia.edu/11"
]

# Function to generate a URL with a random 7-digit numerical string
def generate_random_url():
    base_url = random.choice(base_urls)  # Randomly select a base URL
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    return f"{base_url}{random_digits}"

# Function to make a request to the generated URL
def make_request():
    url = generate_random_url()
    try:
        response = requests.get(url)
        print(f"Requested: {url} | Status Code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")

# Main function to create threads and run multiple requests concurrently
def run_concurrent_requests(num_threads):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
        time.sleep(0.1)  # slight delay to stagger requests

    for thread in threads:
        thread.join()

# Run the script with the desired number of threads
if __name__ == "__main__":
    num_threads = 50000  # Adjust the number of concurrent requests as needed
    run_concurrent_requests(num_threads)
