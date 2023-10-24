from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Pref
from .serializers import PrefSerializer

class All_prefs(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # The alternative: using "if request.user.is_authenticated: ..." for manually deciding which logic require authentication

    def get(self, request):
        allSerializedPosts = PrefSerializer(Pref.objects.filter(user = request.user), many=True).data
        return Response(allSerializedPosts)
    
    def post(self, request):
        try:
            new_pref = Pref(user = request.user, pref_string = request.data['pref_string'], college = request.data['college'], mealtime = request.data['mealtime'], day = request.data['day'])
        except:
            return Response("invalid request body", status=HTTP_400_BAD_REQUEST)
        # Ensure the coordinates are accurate before saving into the database
        new_pref.full_clean()
        new_pref.save()
        return Response(PrefSerializer(new_pref).data, status=HTTP_201_CREATED)
        
class A_pref(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, prefid):
        return Response(PrefSerializer(get_object_or_404(Pref, id = prefid, user = request.user)).data)
    
    def delete(self, request, prefid):
        pref = get_object_or_404(Pref, id = prefid, user = request.user)
        pref.delete()
        return Response("deleted successfully", status=HTTP_204_NO_CONTENT)
