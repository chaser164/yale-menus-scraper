import smtplib
from django.db.models import Count, Q
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv
from user_app.models import User


def send_emails():
    print("initiating email sendouts...")
    # Only select verified, pref-having users
    users = User.objects.filter(verification="verified", prefs__isnull=False)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        load_dotenv()
        server.login('ymenus.scraper@gmail.com', os.getenv('APP_PASSWORD'))
        for user in users:
            msg = MIMEMultipart()
            msg['Subject'] = f'YOUR {datetime.now().month}/{datetime.now().day} YALE MENUS SCRAPE'
            msg['From'] = 'ymenus.scraper@gmail.com'
            msg['To'] = user.email

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