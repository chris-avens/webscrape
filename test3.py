import requests
from bs4 import BeautifulSoup
import time
import argparse


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    html_content = fetch_webpage(args.url)

    if args.condition and args.condition == 'gsm':
        # url = "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php"
        results = parse_gsm(html_content)
        [print(x) for x in results]
    else:
        elements = parse_html(html_content, args.selector)
        for i, element in enumerate(elements, start=1):
            print(f"{i}: {element.text.strip()}")
    
    # Optional: Pause between requests to avoid being blocked
    time.sleep(2)


def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Webscraping")
    parser.add_argument('-u', '--url', required=True, help='URL to scrape')
    parser.add_argument('-s', '--selector', help='CSS selector')
    parser.add_argument('-w', '--wait', type=int, default=10, help='Max wait time in seconds (default=10)')
    parser.add_argument('-c', '--condition', help='Text condition to filter links (optional)')

    return parser


def fetch_webpage(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[fetch_webpage] Error fetching {url}: {e}")
        return None


def parse_html(content, css_selector):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.select(css_selector)
        return elements
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []


def parse_gsm(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        tags = []
        tables = soup.select('div#specs-list > table')
        
        for table in tables:
            trs = table.find_all('tr')
            for tr in trs:
                tds = tr.find_all('td')
                if tds:
                    spec = {
                        "category": table.find('th').text.strip(),
                        "sub-category": tds[0].text.strip(),
                        "detail": tds[1].text.strip(),
                    }
                    tags.append(spec)
        
        return tags
    
    except Exception as e:
        print(f"[parse_gsm] Error parsing HTML: {e}")


if __name__ == "__main__":
    main()