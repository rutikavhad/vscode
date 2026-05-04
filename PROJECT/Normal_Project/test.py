import requests

url = "http://127.0.0.1:8000"

try:
    response = requests.get(url, timeout=5)  # timeout avoids hanging forever
    response.raise_for_status()  # raises HTTPError for 4xx/5xx status codes
    print("GOOD TO GO", response.status_code)
except requests.exceptions.ConnectionError:
    print(f"ERROR: Cannot connect to {url}. Server may be down or URL is wrong.")
except requests.exceptions.Timeout:
    print(f"ERROR: Connection to {url} timed out.")
except requests.exceptions.HTTPError as e:
    print(f"ERROR: HTTP error occurred: {e}")
except requests.exceptions.RequestException as e:
    # Catch all other requests exceptions
    print(f"ERROR: Something went wrong: {e}")