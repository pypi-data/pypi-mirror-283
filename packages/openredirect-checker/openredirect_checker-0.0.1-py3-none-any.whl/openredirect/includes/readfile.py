from openredirect.includes import scan
import requests
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def reader(input, output=None):
    if not input:
        print("must enter the -o for file input ")
        return

    try:
        with open(input, 'r') as file:
            for line in file:
                url = line.strip()
                if is_valid_url(url):
                    try:
                        response = requests.get(url, timeout=5)
                        if response.status_code == 200:
                            scan.openrescan(url, output)
                        else:
                            print(f"URL {url} returned status code {response.status_code}")
                    except (requests.ConnectionError, requests.Timeout):
                        print(f"Connection error or timeout for URL {url}")
                else:
                    print(f"Invalid URL: {url}")
    except FileNotFoundError:
        print("File not found. Check the file path and name.")
