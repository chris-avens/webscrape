import requests
from bs4 import BeautifulSoup
import time


def main():
    url = "https://www.gsmarena.com/res.php3?sSearch=s24+ultra"
    tag = "ul li a"
    scrape_website(url, tag, delay=2)


def fetch_webpage(url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[fetch_webpage] Error fetching {url}: {e}")
        return None


def parse_html(content, tag, attrs=None):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        # elements = soup.find_all(tag, attrs=attrs)  # Find all elements by tag and attributes
        elements = soup.select(tag)
        return elements
    except Exception as e:
        print(f"[parse_html] Error parsing HTML: {e}")
        return []


def scrape_website(url, tag, attrs=None, delay=1):
    # Define headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Fetch webpage
    html_content = fetch_webpage(url, headers)

    if html_content:
        # Parse the HTML
        elements = parse_html(html_content, tag, attrs)

        # Extract and print the relevant data
        for i, element in enumerate(elements, start=1):
            # print(f"{i}: {element.text.strip()}")
            print(f"{i}: {element.get('href')}")

        # Optional: Pause between requests to avoid being blocked
        time.sleep(delay)


if __name__ == "__main__":
    main()