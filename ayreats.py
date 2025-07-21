import base64
import requests
import sys
import time

# Fixed bucket that you know is accepted
BUCKET = "redbox-gbp-img-staging"  # or "redbox-gbp-img-test"

# Max key index from CLI or default to 99
try:
    max_key = int(sys.argv[1])
except (IndexError, ValueError):
    max_key = 10000

ENDPOINT = "https://www.ayreats.co.uk/img/"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Python script)"
}

for k in range(max_key + 1):
    key = f"test{k}"
    payload = {
        "bucket": BUCKET,
        "ke": key  # note lowercase 'ke'
    }
    # Encode JSON-like string with double quotes, standard base64 with padding
    payload_str = str(payload).replace("'", '"')
    encoded = base64.b64encode(payload_str.encode()).decode()

    url = ENDPOINT + encoded
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"[{response.status_code}] BUCKET: {BUCKET} | KE: {key} → {url}")
        # Print part of response if 400 or 403 to debug
        if response.status_code in (400, 403):
            print("Response:", response.text)
    except Exception as e:
        print(f"[ERROR] KE: {key} → {url} : {e}")

    # Optional delay to avoid hammering server too fast
    time.sleep(0.1)
