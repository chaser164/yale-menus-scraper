from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

EXPIRATION_TIME = 300

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.TextField(max_length=500, default='')
    # notice the absence of a "Password field", that is built in.
    # django uses the 'username' to identify users by default, but many modern applications use 'email' instead
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def update_timestamp(self):
        self.timestamp = timezone.now()
        self.save()

    def is_expired(self):
        current_time = timezone.now()
        time_difference = current_time - self.created_at
        return time_difference.total_seconds() > EXPIRATION_TIME
    
    def send_email(self):
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            load_dotenv()
            server.login('yalemenusscraper@gmail.com', os.getenv('APP_PASSWORD'))
            msg = MIMEMultipart()
            msg['Subject'] = f'Yale Menus Scrape Verification Email'
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
