import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time as t
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

LOAD_TIME = 1

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
        service = ChromeService(executable_path=ChromeDriverManager().install())
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
                breakfast_button = driver.find_element(By.ID, "gwt-uid-2")
                dinner_button = driver.find_element(By.ID, "gwt-uid-3")
                brunch_lunch_button = driver.find_element(By.ID, "gwt-uid-4")
            except:
                print(f'Error accessing menu contents of{menu}')
                return

            # Get breakfast page source   
            breakfast_button.click()
            t.sleep(LOAD_TIME)
            breakfast_page_source = driver.page_source
            # get brunch lunch page source
            brunch_lunch_button.click()
            t.sleep(LOAD_TIME)
            brunch_lunch_page_source = driver.page_source
            # Get dinner page source
            dinner_button.click()
            t.sleep(LOAD_TIME)
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
        users = User.objects.all()
        

        msg = MIMEMultipart()
        msg['Subject'] = 'Today\'s Yale Menus Readout'
        msg['From'] = 'yalemenusreadout@gmail.com'
        msg['To'] = "creynders22@gmail.com"

        # HTML content for the email body
        html_body = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My Web Page</title>
            <style>
                .big-blue-button {{
                    display: inline-block;
                    padding: 15px 30px;
                    background-color: #a8dcff;
                    color: white;
                    text-decoration: none;
                    border: none;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                }}

                .big-blue-button:hover {{
                    background-color: #7dc2f3;
                }}
            </style>
        </head>
        <body>
            <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                    <td align="center">
                        <h1>Welcome to GutCheck!</h1>
                        <h2>Please click the button to confirm your email:</h2>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <p>hello</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        # Attach the HTML content to the email message
        html_part = MIMEText(html_body, "html")
        msg.attach(html_part)

        # Send the message via our own SMTP server.
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        username = 'yalemenusreadout@gmail.com'
        # app-specific password, per google's requirements (stored in .env file)
        load_dotenv()
        password = os.getenv('APP_PASSWORD')

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            print("Email sent successfully!")
            # Only save database upon successful email send
        except Exception as e:
            print(e)
            print("Error sending email")
