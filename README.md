# Yale Menus Scraper

## **TODO:**
- Work on email confirmation (just send a 6 digit code it's easier...)
- Allow account deletion
- updating/deleting prefs
- cookie auth
- writing out API endpoints

## **API ENDPOINTS**

### **api/v1/prefs/**
+ __GET__ returns all preferences of the user
+ __POST__ creates a preference
### **api/v1/int:prefid/**
+ __GET__ returns preference, must belong to the caller
+ __DELETE__ deletes preference, must belong to the caller
### **api/v1/users/signup/**
+ __POST__ signs up a user
### **api/v1/users/login/**
+ __POST__ log in a user
### **api/v1/users/logout/**
+ __POST__ log out a user
### **api/v1/users/admin-signup/**
+ __POST__ log in a user
### **api/v1/users/**
+ __GET__ returns info about all users
### **api/v1/users/me/**
+ __GET__ returns info about self
### **api/v1/users/int:userid/**
+ __GET__ returns info about specific id
+ __DELETE__ deletes user with certain ID, admin access only