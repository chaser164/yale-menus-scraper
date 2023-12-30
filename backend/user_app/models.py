from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
import os
import hashlib
import random
from twilio.rest import Client
from dotenv import load_dotenv

EXPIRATION_TIME = 300

class User(AbstractUser):
    phone = models.PositiveBigIntegerField(unique=True)
    verification_timestamp = models.DateTimeField(auto_now_add=True)
    reset_timestamp = models.DateTimeField(auto_now_add=True)
    verification = models.TextField(max_length=500, default='')
    reset = models.TextField(max_length=500, default='')
    # notice the absence of a "Password field", that is built in.
    # django uses the 'username' to identify users by default, but many modern applications use 'email' instead
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = [] # Email & Password are required by default.

    def check_code(self, code, for_reset):
        if User.hash(code) != (self.reset if for_reset else self.verification):
            return "invalid code"
        elif self.is_expired(for_reset):
            return "expired code"
        else:
            if for_reset:
                self.reset = "verified"
            else:
                self.verification = "verified"
            self.save()
            return "valid code"


    def is_expired(self, for_reset):
        current_time = timezone.now()
        if for_reset:
            time_difference = current_time - self.reset_timestamp
        else:
            time_difference = current_time - self.verification_timestamp
        return time_difference.total_seconds() > EXPIRATION_TIME
    
    # Send text with 6 digit code
    def send_text(self, for_reset):
        account_sid = 'ACcb94a77d070d8e1e065eb9c0e9647142'
        load_dotenv()
        auth_token = os.getenv('AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            messaging_service_sid='MG111ded7875b2fa3b99d8688c939a8843',
        body=self.generate_code(for_reset),
        to=f'+{self.phone}'
        )
        # Update timestamp
        if for_reset:
            self.reset_timestamp = timezone.now()
        else:
            self.verification_timestamp = timezone.now()
        self.save()

    # Sends email with 6 digit code
    # populates "verification" field with hashed 6 digit code
    # Updates timestamp to now if email is sent successfully
    # def send_email(self, for_reset):
    #     with smtplib.SMTP('smtp.gmail.com', 587) as server:
    #         server.starttls()
    #         load_dotenv()
    #         server.login('ymenus.scraper@gmail.com', os.getenv('APP_PASSWORD'))
    #         msg = MIMEMultipart()
    #         msg['Subject'] = f'Yale Menus Scraper Verification Email'
    #         msg['From'] = 'ymenus.scraper@gmail.com'
    #         msg['To'] = self.email
    #         # Attach the html
    #         text = MIMEText(self.generate_code(for_reset), 'html')
    #         msg.attach(text)
    #         # Send email
    #         server.send_message(msg)
    #         if for_reset:
    #             self.reset_timestamp = timezone.now()
    #         else:
    #             self.verification_timestamp = timezone.now()
    #         self.save()


    def generate_code(self, for_reset):
        # Generate code
        code = random.randint(100000, 999999)
        hashed_code = User.hash(code)
        # Save hashed code in database
        if for_reset:
            self.reset = hashed_code
        else:
            self.verification = hashed_code
        self.save()
        return f"""
            Your Yale Menus Scraper {"password reset" if for_reset else "account activation"} code is {str(code)}
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