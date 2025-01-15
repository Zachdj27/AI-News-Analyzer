from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import re

def fetch_article_content(url):
    options = Options()
    # options.add_argument('--headless')  
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')  
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')  
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    driver = webdriver.Chrome(options=options)  
    driver.get(url)
    
    #disable automation detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    #wait for page to load
    time.sleep(0.5)

    #handle the "Accept all cookies" button
    try:
        accept_all_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.secondary.accept-all'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", accept_all_button)
        ActionChains(driver).move_to_element(accept_all_button).click().perform()
        print("Clicked 'Accept all' button.")
        time.sleep(0.5)  
    except TimeoutException:
        print("Cookie consent overlay missing or already accepted.")

    #handle "Continue Reading" button
    try:
        continue_reading_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.secondary-btn.continue-reading-button'))
        )
        print("Redirect button found. Returning -1 to indicate redirection.")
        driver.quit()
        return None
    except TimeoutException:
        print("No 'Continue Reading' button found.")

    #handle "Read more" button
    try:
        read_more_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.readmore-button'))
        )
        print("Found 'Read more' button, clicking it.")
        driver.execute_script("arguments[0].scrollIntoView();", read_more_button)
        ActionChains(driver).move_to_element(read_more_button).click().perform()
        time.sleep(0.5)
    except TimeoutException:
        print("No 'Read more' button found.")

    #extract article content
    try:
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        body_div = soup.find('div', class_=re.compile(r'^body yf-'))
        if body_div:
            paragraphs = body_div.find_all('p')
            article_content = "\n".join(p.get_text() for p in paragraphs)
            driver.quit()
            return article_content
        else:
            print("Article body not found.")
            driver.quit()
            return None
    except Exception as e:
        print("Error extracting article content:", e)
        driver.quit()
        return None

