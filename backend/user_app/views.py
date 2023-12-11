#user_app.views
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class Sign_up(APIView):
    
    def post(self, request):
        request.data["username"] = request.data["email"]
        try:
            user = User.objects.create_user(**request.data)
            user.send_verification_email()
        except:
            return Response("Email already in use", status=HTTP_400_BAD_REQUEST)
        token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(user).data}, status=HTTP_201_CREATED
        )
    
class Log_in(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": UserSerializer(user).data})
        else:
            return Response("No user matching credentials", status=HTTP_404_NOT_FOUND)

class Log_out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class Admin_sign_up(APIView):
    # MAKE THIS A MORE SECURE PAGE...

    def post(self, request):
        admin_user = User.objects.create_user(**request.data)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        token = Token.objects.create(user=admin_user)
        return Response(
            {"admin_user": admin_user.username, "token": token.key}, status=HTTP_201_CREATED
        )

class All_users(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

     # Only admins (users that are both staff and superusers) may view the master list of all users
    def get(self, request):
        if request.user.is_staff and request.user.is_superuser:
            return Response(UserSerializer(User.objects.all(), many=True).data)
        else:
            return Response("Admin access only", status=HTTP_401_UNAUTHORIZED)
        
class A_user(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, userid=None):
        if userid is not None:
            user = get_object_or_404(User, id = userid)
            return Response(UserSerializer(user).data)
        else:
            # Accessing your own info with "me" endpoint
            return Response(UserSerializer(request.user).data)
        
    # Only admins (users that are both staff and superusers) may delete other users
    def delete(self, request, userid):
        if request.user.is_staff and request.user.is_superuser:
            user = get_object_or_404(User, id = userid)
            if user == request.user:
                return Response("Cannot delete yourself", status=HTTP_401_UNAUTHORIZED)
            if user.is_staff and user.is_superuser:
                return Response("Cannot delete other admins", status=HTTP_401_UNAUTHORIZED)
            else:
                user.delete()
                return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response("Admin access only", status=HTTP_401_UNAUTHORIZED)
        

class Validate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        code = request.data["code"]
        message = request.user.check_code(code)
        is_valid = message == "valid code"
        return Response(
            {"message": message, "is_valid": is_valid}
        )
    
class Resend(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        return Response(
            {"message": request.user.send_verification_email()}
        )