
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import argparse


def main():
    args = setup_argument_parser().parse_args()
    search_string = '+'.join(args.keywords)
    result = search_gsmarena(search_string)
    print(result)


def search_gsmarena(search_string):
    driver = webdriver.Chrome()
    driver.get(f'https://www.gsmarena.com/res.php3?sSearch={search_string}')

    try:
        a_tags = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#review-body a')))
        return [a_tag.get_attribute('href') for a_tag in a_tags]
    except TimeoutException:
        print("Timed out waiting for elements to load")
    finally:
        driver.quit()


def setup_argument_parser():
    parser = argparse.ArgumentParser(description='Search with multiple keywords')
    parser.add_argument('keywords', nargs='+', help='Search keywords (one or more)')
    return parser


if __name__ == "__main__":
    main()