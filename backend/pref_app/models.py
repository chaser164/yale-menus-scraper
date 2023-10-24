from django.db import models
from user_app.models import User

# Create your models here.
class Pref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prefs')
    pref_string = models.CharField(max_length=300)
    colleges = models.CharField(max_length=42, blank=True, null=True)
    mealtimes = models.CharField(max_length=20, blank=True, null=True)
