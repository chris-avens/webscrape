import requests
from bs4 import BeautifulSoup
import time
import json


def main():
    url = "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php"
    tag = "td"
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
        elements = soup.find_all(tag, attrs=attrs)  # Find all elements by tag and attributes
        return elements
    except Exception as e:
        print(f"[parse_html] Error parsing HTML: {e}")
        return []


def parse_gsm(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        specs_list = soup.find('div', id='specs-list')
        tags = []
        if specs_list:
            tables = specs_list.find_all('table')
            
            for i, table in enumerate(tables, start=1):
                th = table.find('th')
                trs = table.find_all('tr')
                for j, tr in enumerate(trs, start=1):
                    tds = tr.find_all('td')
                    # print(f"{i}: {th.text.strip()}")
                    if tds:
                        spec = {
                            "category": th.text.strip(),
                            "sub-category": tds[0].text.strip(),
                            "detail": tds[1].text.strip(),
                        }
                        tags.append(spec)

                # if th:
                #     print(f"{i}: {th.text.strip()}")
                #     tags.append(th.text.strip())
            
            [print(x) for x in tags]
        else:
            print("No <div> with id='info-div' found.")
    
    except Exception as e:
        print(f"[parse_gsm] Error parsing HTML: {e}")


def scrape_website(url, tag, attrs=None, delay=1):
    # Define headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Fetch webpage
    html_content = fetch_webpage(url, headers)

    if html_content:
        # Parse the HTML
        # elements = parse_html(html_content, tag, attrs)
        elements = parse_gsm(html_content)

        # Extract and print the relevant data
        # for i, element in enumerate(elements, start=1):
        #     print(f"{i}: {element.text.strip()}")

        # Optional: Pause between requests to avoid being blocked
        time.sleep(delay)


if __name__ == "__main__":
    main()