import re
import time as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from django.core.management.base import BaseCommand
from pref_app.models import Pref
from .email import send_emails

LOAD_TIME = 0.15

menus = {
    ' BK':1,
    ' BR & SB':2,
    ' DP':3,
    ' ES & MO':4,
    ' BF & PM':5,
    ' GH':6,
    ' JE':7,
    ' PS':8,
    ' SM':9,
    ' TD':10,
    ' TB':11,
}

class Command(BaseCommand):
    help = 'Update all fields of Pref to reflect the current day\'s options'

    def handle(self, *args, **options):
        print("initiating update...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get("https://www.google.com")
            print("Page title was '{}'".format(driver.title))
        finally:
            driver.quit()
        # prefs = Pref.objects.all()

        # for menu in menus:
        #     driver.get(f'https://usa.jamix.cloud/menu/app?anro=97939&k={menus[menu]}')
        #     # Attempt to access menu and configure buttons
        #     try:
        #         # Find and click the agreement-to-terms button
        #         driver.implicitly_wait(10)
        #         view_button = driver.find_element(By.CSS_SELECTOR, '[class="v-button v-widget multiline v-button-multiline selection v-button-selection icon-align-right v-button-icon-align-right v-has-width"]')
        #         view_button.click()
        #         # Allow time for the menu loading animation
        #         driver.implicitly_wait(10)
        #         meals = driver.find_elements(By.CLASS_NAME, "v-captiontext")
        #         if len(meals) == 3:
        #             breakfast_button = meals[0]
        #             dinner_button = meals[1]
        #             brunch_lunch_button = meals[2]
        #         else:
        #             breakfast_button = None
        #             dinner_button = meals[0]
        #             brunch_lunch_button = meals[1]
        #     except:
        #         print(f'timeout while entering{menu} menu')
        #         driver.quit()
        #         return

        #     # Account for optionality of breakfast
        #     if breakfast_button != None:
        #         # Get breakfast page source   
        #         breakfast_button.click()
        #         # Wait until menu contents loaded by checking for header presence
        #         total = 0
        #         while not '<title>Breakfast' in driver.page_source:
        #             t.sleep(LOAD_TIME)
        #             total += LOAD_TIME
        #             if total > 10:
        #                 print(f'timeout while retrieving Breakfast menu for{menu}')
        #                 driver.quit()
        #                 return
        #             continue
        #         breakfast_page_source = driver.page_source
        #     else:
        #         breakfast_page_source = ""
        #     # Get dinner page source
        #     dinner_button.click()
        #     # Wait until menu contents loaded by checking for header presence
        #     total = 0
        #     while not '<title>Dinner' in driver.page_source:
        #         t.sleep(LOAD_TIME)
        #         total += LOAD_TIME
        #         if total > 10:
        #             print(f'timeout while retrieving Dinner menu for{menu}')
        #             driver.quit()
        #             return
        #         continue
        #     dinner_page_source = driver.page_source
        #     # get brunch lunch page source
        #     brunch_lunch_button.click()
        #     # Wait until menu contents loaded by checking for header presence
        #     total = 0
        #     while not '<title>Brunch and Lunch' in driver.page_source:
        #         t.sleep(LOAD_TIME)
        #         total += LOAD_TIME
        #         if total > 10:
        #             print(f'timeout while retrieving Brunch/Lunch menu for{menu}')
        #             driver.quit()
        #             return
        #         continue
        #     brunch_lunch_page_source = driver.page_source
            
        #     for pref in prefs:
        #         # Add breakfast data
        #         if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', breakfast_page_source, re.IGNORECASE):
        #             pref.breakfast += menu
        #         # Add brunch/lunch data
        #         if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', brunch_lunch_page_source, re.IGNORECASE):
        #             pref.brunch_lunch += menu
        #         # Add dinner data
        #         if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', dinner_page_source, re.IGNORECASE):
        #             pref.dinner += menu
        #         pref.save()
        #     print(f'{menu[1:]} data added...')

        # driver.quit()
        # print('fields update complete!')

        # send_emails()
        