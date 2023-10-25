from django.core.management.base import BaseCommand
from pref_app.models import Pref

class Command(BaseCommand):
    help = 'Empty all fields'

    def handle(self, *args, **options):
        prefs = Pref.objects.all()
        for pref in prefs:
            pref.breakfast = ""
            pref.brunch_lunch = ""
            pref.dinner = ""
            pref.save()