from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
import re


def fetch_article_content(url):
    
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Disabling GPU can improve speed in some cases
    options.add_argument('--no-sandbox')  # Can help avoid issues in some environments
    options.add_argument('--disable-dev-shm-usage')  # Helps prevent resource issues
    driver = webdriver.Chrome(options=options)  # Ensure you have the correct driver installed
    driver.get(url)
    
    # Handle the "Accept all cookies" button
    try:
        
        accept_all_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.secondary.accept-all'))
        )
        
        # Scroll into view 
        driver.execute_script("arguments[0].scrollIntoView();", accept_all_button)
        ActionChains(driver).move_to_element(accept_all_button).click().perform()
        print("Clicked 'Accept all' button.")
    except TimeoutException:
        print('Cookie consent overlay missing')

    # Handle "Continue Reading" button 
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.secondary-btn.continue-reading-button'))
        )
        print("Redirect button found. Returning -1 to indicate redirection.")
        driver.quit()  
        return -1
    except Exception as e:
        print("No 'Continue Reading' button found")

    # Handle "Read more" button 
    try:
        read_more_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.readmore-button'))
        )
        print("Found 'Read more' button, clicking it.")
        ActionChains(driver).move_to_element(read_more_button).click().perform()
    except Exception as e:
        print("No 'Read more' button found or other issue:")
        
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find body of text
        body_div = soup.find('div', class_=re.compile(r'^body yf-'))

        if body_div:
            # Extract all paragraphs inside the body div
            paragraphs = body_div.find_all('p')
            article_content = "\n".join(p.get_text() for p in paragraphs)
            driver.quit()  
            return article_content  
        else:
            print("Article body not found.")
            driver.quit()  
            return None  # If no body content, return None
    except Exception as e:
        print("Error extracting article content:", e)
        driver.quit() 
        return None  # If there is an error, return None

