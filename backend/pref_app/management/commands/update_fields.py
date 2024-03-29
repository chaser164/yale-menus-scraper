import re
import time as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from django.core.management.base import BaseCommand
from pref_app.models import Pref
# from .message import send_emails
from .message import send_texts


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

        prefs = Pref.objects.all()

        for menu in menus:
            driver.get(f'https://usa.jamix.cloud/menu/app?anro=97939&k={menus[menu]}')
            # Attempt to access menu and configure buttons
            try:
                # Find and click the agreement-to-terms button
                driver.implicitly_wait(10)
                view_button = driver.find_element(By.CSS_SELECTOR, '[class="v-button v-widget multiline v-button-multiline selection v-button-selection icon-align-right v-button-icon-align-right v-has-width"]')
                view_button.click()
                # Allow time for the menu loading animation
                driver.implicitly_wait(10)
                meals = driver.find_elements(By.CLASS_NAME, "v-tabsheet-tabitemcell")
                # Create scrollers if need be
                prev_scroller = None
                next_scroller = None
                try:
                    driver.implicitly_wait(5)
                    prev_scroller = driver.find_element(By.CLASS_NAME, 'v-tabsheet-scrollerPrev')
                    next_scroller = driver.find_element(By.CLASS_NAME, 'v-tabsheet-scrollerNext-disabled')
                except:
                    pass
            except:
                print(f'timeout while entering{menu} menu')
                driver.quit()
                return
            page_source_dict_lst = [{'id': '<title>Breakfast', 'visited' : False, 'src': ''},
                                    {'id': '<title>Brunch and Lunch', 'visited' : False, 'src': ''},
                                    {'id': '<title>Dinner', 'visited' : False, 'src': ''}]
            for meal in meals:
                # Scroll until found; click
                clicked = False
                scroll_count = 0
                while(not clicked):
                    try:
                        meal.click()
                        clicked = True
                    except:
                        if(prev_scroller == None or next_scroller == None):
                            print('ERROR: no scrollers found, yet item not visible')
                            return
                        prev_scroller.click()
                        scroll_count += 1
                # reset scroll
                for _ in range(scroll_count):
                    next_scroller.click()
                total = 0
                while True:
                    # Sleep a bit
                    t.sleep(LOAD_TIME)
                    # Populate dict with page src
                    found = False
                    for item in page_source_dict_lst:
                        if item['id'] in driver.page_source and not item['visited']:
                            item['src'] = driver.page_source
                            item['visited'] = True
                            found = True
                            break
                    total += LOAD_TIME
                    # Continue after timeout or menu populated
                    if total > 7 or found:
                        break

            # Add all prefs
            for pref in prefs:
                # Add breakfast data
                if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', page_source_dict_lst[0]['src'], re.IGNORECASE):
                    pref.breakfast += menu
                # Add brunch/lunch data
                if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', page_source_dict_lst[1]['src'], re.IGNORECASE):
                    pref.brunch_lunch += menu
                # Add dinner data
                if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', page_source_dict_lst[2]['src'], re.IGNORECASE):
                    pref.dinner += menu
                pref.save()
            print(f'{menu[1:]} data added...')

        driver.quit()
        print('fields update complete!')

        send_texts()
        