#!/usr/bin/env python3

import requests

# Base URL (without fragment at first)
base_url = "https://canisportsscotland.wordpress.com/"

# Loop from 0001 to 9999
for i in range(1, 10000):
    comment_id = f"{i:04d}"
    # Append the comment fragment
    url_with_fragment = f"{base_url}#comment-{comment_id}"

    # You can optionally show the fragment, but for requests, use the base URL
    print(f"Requesting: {url_with_fragment}")

    try:
        # Make GET request to the base URL (fragment is not sent to server)
        response = requests.get(base_url, timeout=10)

        # Print status code
        print(f"Status code: {response.status_code}")

        # Print headers
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        print("-" * 50)

    except requests.RequestException as e:
        print(f"Error: {e}")
