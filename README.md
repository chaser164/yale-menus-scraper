# Yale Menus Scraper

yale-menus-scraper.com

Welcome to Yale Menus Scraper, a full stack web app that allows Yale eaters to configure personalized food alerts! 

Every day at 6AM EST, the web app runs a (case insensitive) scrape of every Yale residential college dining hall menu. Users will then receive a personalized email digest detailing which of their specified food items are present in the day's menus.

## **API ENDPOINTS**

### **api/v1/prefs/**
+ __GET__ returns all preferences of the user
+ __POST__ creates a preference
### **api/v1/int:prefid/**
+ __GET__ returns preference, must belong to the caller
+ __DELETE__ deletes preference, must belong to the caller
### **api/v1/users/signup/**
+ __POST__ signs up a user, sending verification email
### **api/v1/users/login/**
+ __POST__ log in a user
### **api/v1/users/logout/**
+ __POST__ log out a user
### **api/v1/users/**
+ __GET__ returns info about all users
### **api/v1/users/me/**
+ __GET__ returns info about self
+ __DELETE__ deletes self
### **api/v1/users/int:userid/**
+ __GET__ returns info about specific id
### **api/v1/users/validate/**
+ __POST__ validate a user's 6-digit pin
### **api/v1/users/validate/**
+ __POST__ resend validation email
### **api/v1/users/init-reset/**
+ __POST__ checks if given email exists. If it does, generate reset pin
### **api/v1/users/validate-reset/**
+ __POST__ check if given reset pin matches. If it does, update the password