import subprocess
from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import CHROME_PATH, CHROME_ARGS


def start_chrome():
    """Start Chrome with remote debugging enabled."""
    subprocess.Popen(f'"{CHROME_PATH}" {CHROME_ARGS}', shell=True, stderr=subprocess.DEVNULL)
    sleep(5)  # Allow some time for Chrome to start


def initialize_driver():
    """Initialize the Selenium WebDriver with predefined options."""
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def login(driver):
    base_url = "https://www.instagram.com/"
    driver.get(base_url)
    input('Press enter when you are logged in.')


def post_comment(driver, post_url, comment_text):
    try:
        driver.get(post_url)
        attempts = 3  # Number of attempts to try finding the element
        for attempt in range(attempts):
            try:
                comment_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//textarea[contains(@aria-label, 'Add a comment')]"))
                )
                comment_box.clear()
                comment_box.send_keys(comment_text)
                # Uncomment and adjust the following lines as needed if posting is required
                post_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(text(), 'Post')]"))
                )
                post_button.click()
                print(f"Comment posted successfully at {post_url}!")
                break  # Break the loop if successful
            except StaleElementReferenceException:
                print(f"Retrying to find element, attempt {attempt + 1}...")
                if attempt == attempts - 1:
                    raise  # Re-raise the exception if the last attempt fails
    except (TimeoutException, Exception) as e:
        print(f"An error occurred while posting the comment: {e}")


def like_post(driver, post_url):
    try:
        driver.get(post_url)
        attempts = 3  # Number of attempts to try finding and clicking the element
        for attempt in range(attempts):
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='Like' and @height='24']"))
                )
                ActionChains(driver).move_to_element(element).click().perform()
                print(f"Element clicked successfully at {post_url}!")
                break  # Break the loop if click was successful
            except StaleElementReferenceException:
                print(f"Element became stale, retrying {attempt + 1} of {attempts}...")
                if attempt == attempts - 1:
                    raise
    except (TimeoutException, Exception) as e:
        print(f"An error occurred while liking the post: {e}")
