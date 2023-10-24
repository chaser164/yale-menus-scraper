from rest_framework import serializers
from .models import Pref

class PrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pref
        fields = '__all__'
