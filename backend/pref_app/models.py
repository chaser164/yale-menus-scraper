from django.db import models
from user_app.models import User

# Create your models here.
class Pref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prefs')
    pref_string = models.CharField(max_length=250)
    college = models.CharField(max_length=2, blank=True, null=True)
    mealtime = models.CharField(max_length=10, blank=True, null=True)
    day = models.CharField(max_length=21, blank=True, null=True)

