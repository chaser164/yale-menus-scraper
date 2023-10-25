from django.db import models
from user_app.models import User

# Create your models here.
class Pref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prefs')
    pref_string = models.CharField(max_length=300)
    breakfast = models.CharField(max_length=50, default = "")
    brunch_lunch = models.CharField(max_length=50, default = "")
    dinner = models.CharField(max_length=50, default = "")
