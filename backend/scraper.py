import time as t
import os
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = ChromeService(executable_path=ChromeDriverManager().install())
chrome_options = Options()
# chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options, service=service)


def main():
    driver.get('https://usa.jamix.cloud/menu/app?anro=97939&k=1')
    # Attempt to access menu and configure buttons
    try:
        driver.implicitly_wait(10)
        # Find and click the agreement-to-terms button
        view_button = driver.find_element(By.CSS_SELECTOR, '[class="v-button v-widget multiline v-button-multiline selection v-button-selection icon-align-right v-button-icon-align-right v-has-width"]')
        view_button.click()
        # Allow time for the menu loading animation
        driver.implicitly_wait(10)
        breakfast_button = driver.find_element(By.ID, "gwt-uid-2")
        dinner_button = driver.find_element(By.ID, "gwt-uid-3")
        brunch_lunch_button = driver.find_element(By.ID, "gwt-uid-4")
    except:
        print("Error accessing menu contents")
        return 1

    breakfast_button.click()
    t.sleep(3)
    print('Oatmeal' in driver.page_source)
    t.sleep(5)
    driver.quit()

main()

