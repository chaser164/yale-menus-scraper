import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time as t
from datetime import datetime
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from django.core.management.base import BaseCommand
from pref_app.models import Pref
from user_app.models import User

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
        try:
            service = ChromeService(executable_path=ChromeDriverManager().install())
        except:
            print("Offline. Exiting.")
            return
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options, service=service)

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
                breakfast_button = driver.find_element(By.ID, "gwt-uid-2") # might not always be here during weekends ... consider v-captiontext
                dinner_button = driver.find_element(By.ID, "gwt-uid-3")
                brunch_lunch_button = driver.find_element(By.ID, "gwt-uid-4")
            except:
                print(f'timeout while entering{menu} menu')
                driver.quit()
                return

            # Get breakfast page source   
            breakfast_button.click()
            # Wait until menu contents loaded by checking for header presence
            total = 0
            while not '<title>Breakfast' in driver.page_source:
                t.sleep(LOAD_TIME)
                total += LOAD_TIME
                if total > 10:
                    print(f'timeout while retrieving Breakfast menu for{menu}')
                    driver.quit()
                    return
                continue
            breakfast_page_source = driver.page_source
            # get brunch lunch page source
            brunch_lunch_button.click()
            # Wait until menu contents loaded by checking for header presence
            total = 0
            while not '<title>Brunch and Lunch' in driver.page_source:
                t.sleep(LOAD_TIME)
                total += LOAD_TIME
                if total > 10:
                    print(f'timeout while retrieving Brunch/Lunch menu for{menu}')
                    driver.quit()
                    return
                continue
            brunch_lunch_page_source = driver.page_source
            # Get dinner page source
            dinner_button.click()
            # Wait until menu contents loaded by checking for header presence
            total = 0
            while not '<title>Dinner' in driver.page_source:
                t.sleep(LOAD_TIME)
                total += LOAD_TIME
                if total > 10:
                    print(f'timeout while retrieving Dinner menu for{menu}')
                    driver.quit()
                    return
                continue
            dinner_page_source = driver.page_source
            
            for pref in prefs:
                # Add breakfast data
                if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', breakfast_page_source, re.IGNORECASE):
                    pref.breakfast += menu
                # Add brunch/lunch data
                if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', brunch_lunch_page_source, re.IGNORECASE):
                    pref.brunch_lunch += menu
                # Add dinner data
                if re.search(rf'>[^<]*{pref.pref_string}[^>]*<', dinner_page_source, re.IGNORECASE):
                    pref.dinner += menu
                pref.save()
            print(f'{menu[1:]} data added...')

        driver.quit()
        print('fields update complete!')
        
        # EMAIL SEND
        print("initiating email sendouts...")
        users = User.objects.all()
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            load_dotenv()
            server.login('yalemenusscraper@gmail.com', os.getenv('APP_PASSWORD'))
            for user in users:
                msg = MIMEMultipart()
                msg['Subject'] = f'YOUR {datetime.now().month}/{datetime.now().day} YALE MENUS SCRAPE'
                msg['From'] = 'yalemenusscraper@gmail.com'
                msg['To'] = "creynders22@gmail.com"

                # Attach the html
                text = MIMEText(build_message_html(user.prefs), 'html')
                msg.attach(text)
                try:
                    server.send_message(msg)
                    print(f"Email to {user.email} sent successfully")
                except:
                    print(f"Error sending email for {user.email}")
        print("All emails sent!")


def build_message_html(user_prefs):
    colleges = {
        'BK':'Berkeley ',
        'BR':'Branford ',
        'SB':'Saybrook ',
        'DP':'Davenport ',
        'ES':'Stiles ',
        'MO':'Morse ',
        'BF':'Franklin ',
        'PM':'Murray ',
        'GH':'Hopper ',
        'JE':'JE ',
        'PS':'Pierson ',
        'SM':'Silliman ',
        'TD':'TD ',
        'TB':'Trumbull '
    }
    all_results = ''
    for pref in user_prefs.all():
        found_anywhere = False
        result = f"""<div style="text-align: left; font-size: large;">Results for <b>"{pref.pref_string}"</b>:</div> <br>
        <table width="50%" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center">
                    <div style="text-align: right;">
        """
        for col in colleges:
            found_in_college = False
            col_string = colleges[col]
            if col in pref.breakfast:
                found_in_college = True
                col_string += '⏰'
            else:
                col_string += '&nbsp;&nbsp;'
            if col in pref.brunch_lunch:
                found_in_college = True
                col_string += '☀️'
            else:
                col_string += '&nbsp;&nbsp;'
            if col in pref.dinner:
                found_in_college = True
                col_string += '🌙'
            else:
                col_string += '&nbsp;&nbsp;'
            # Ensure found in college
            if found_in_college:
                found_anywhere = True
                result += col_string + '<br>'
        if found_anywhere:
            all_results += result + '</div></td></tr></table><br><br><br><br><hr><br>'
        else:
            all_results += f'<div style="text-align: left; font-size: large;">No results for <b>"{pref.pref_string}"</b></div><br><br><br><hr><br>'

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: monospace, monospace;">
        <div style="text-align: left;">
            ⏰  =  Appears in <b>breakfast menu</b><br>
            ☀️  = Appears in <b>brunch/lunch menu</b><br>
            🌙  = Appears in <b>dinner menu</b><br>
            <br><br><br>
            <hr>
        </div>
        {all_results}
    </body>
    </html>
    """