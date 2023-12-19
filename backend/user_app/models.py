from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import hashlib
import random
from dotenv import load_dotenv

EXPIRATION_TIME = 300

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    verification = models.TextField(max_length=500, default='')
    # notice the absence of a "Password field", that is built in.
    # django uses the 'username' to identify users by default, but many modern applications use 'email' instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def check_code(self, code):
        if User.hash(code) != self.verification:
            return "invalid code"
        elif self.is_expired():
            return "expired code"
        else:
            self.verification = "verified"
            self.save()
            return "valid code"


    def is_expired(self):
        current_time = timezone.now()
        time_difference = current_time - self.timestamp
        return time_difference.total_seconds() > EXPIRATION_TIME

    # Sends email with 6 digit code
    # populates "verification" field with hashed 6 digit code
    # Updates timestamp to now if email is sent successfully
    def send_verification_email(self):
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            load_dotenv()
            server.login('yalemenusscraper@gmail.com', os.getenv('APP_PASSWORD'))
            msg = MIMEMultipart()
            msg['Subject'] = f'Yale Menus Scrape Verification Email'
            msg['From'] = 'yalemenusscraper@gmail.com'
            msg['To'] = self.email
            # Attach the html
            text = MIMEText(self.generate_code(), 'html')
            msg.attach(text)
            # Send email
            server.send_message(msg)
            self.timestamp = timezone.now()
            self.save()


    def generate_code(self):
        # Generate code
        code = random.randint(100000, 999999)
        hashed_code = User.hash(code)
        # Save hashed code in database
        self.verification = hashed_code
        self.save()
        return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body >
                <table width="50%" cellspacing="0" cellpadding="0">
                <tr>
                    <h1>Yale Menus Scraper Email Confirmation</h1>
                </tr>
                <tr>
                    <p>Your code is</p>
                    <b>{str(code)}</b>
                </tr>
                </table>
            </body>
            </html>
        """

    @staticmethod
    def hash(input):
        m = hashlib.sha1()
        #stringify
        input = str(input)
        #encode
        encoded_input = input.encode('utf-8')
        #hash
        m.update(encoded_input)
        hash_output = m.hexdigest()
        return hash_output