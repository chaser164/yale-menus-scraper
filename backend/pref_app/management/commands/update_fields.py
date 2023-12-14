import re
import time as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from django.core.management.base import BaseCommand
from pref_app.models import Pref
from .email import send_emails
from chromedriver_autoinstaller import install as install_chromedriver

LOAD_TIME = 0.15

menus = {
    ' BK': 1,
    ' BR & SB': 2,
    ' DP': 3,
    ' ES & MO': 4,
    ' BF & PM': 5,
    ' GH': 6,
    ' JE': 7,
    ' PS': 8,
    ' SM': 9,
    ' TD': 10,
    ' TB': 11,
}

class Command(BaseCommand):
    help = 'Update all fields of Pref to reflect the current day\'s options'

    def handle(self, *args, **options):
        print("initiating update...")

        # Install Chromium WebDriver
        install_chromedriver()

        try:
            # Use Chromium WebDriver
            service = ChromeService(executable_path=ChromeDriverManager(chrome_type="chromium", version='114.0.5735.90').install())
        except:
            print("Offline. Exiting.")
            return

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options, service=service)

        # Rest of your code remains unchanged
        # ...

        driver.quit()
        print('fields update complete!')

        send_emails()
