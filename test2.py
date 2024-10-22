
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.get('https://www.gsmarena.com/res.php3?sSearch=s24+ultra')

# Method 1: Using CSS Selector (recommended)
# This gets all <a> tags inside #info-div, no matter how deep
a_tags = driver.find_elements(By.CSS_SELECTOR, '#review-body a')

# Method 2: Using XPath
# The // means it will find <a> tags at any depth inside the div
a_tags = driver.find_elements(By.XPATH, "//div[@id='review-body']//a")

# It's better to wait for elements to load instead of using time.sleep
try:
    # Wait up to 10 seconds for elements to be present
    a_tags = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#review-body a'))
    )
    
    # Print all found links
    for i, a_tag in enumerate(a_tags, start=1):
        href = a_tag.get_attribute('href')
        text = a_tag.text
        print(f"{i}: {href}")

except TimeoutException:
    print("Timed out waiting for elements to load")

finally:
    driver.quit()