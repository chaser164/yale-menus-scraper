from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer): 
    is_verified = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'phone', 'prefs', 'is_verified']

    def get_is_verified(self, obj):
        return obj.verification == "verified"