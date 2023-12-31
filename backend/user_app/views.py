from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utilities import HttpOnlyTokenAuthentication

from .models import User
from .serializers import UserSerializer


class Sign_up(APIView):
    
    def post(self, request):
        # Add user attempt
        try:
            user = User.objects.create_user(**request.data)
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower() and 'username' in str(e).lower():
                return Response({"message": "Username already in use"}, status=HTTP_400_BAD_REQUEST)
            elif 'unique constraint' in str(e).lower() and 'phone' in str(e).lower():
                return Response({"message": "Phone number already in use"}, status=HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Unknown error"}, status=HTTP_400_BAD_REQUEST)
        # Send text attempt
        try:
            user.send_text(False)
        except:
            user.delete()
            return Response({"message": "Error sending text, try again"}, status=HTTP_400_BAD_REQUEST)
        token = Token.objects.create(user=user)
        life_time = datetime.now() + timedelta(days=7)
        format_life_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response = Response({"user": UserSerializer(user).data})
        response.set_cookie(key="token", value=token.key, httponly=True, secure=True, samesite="Strict", expires=format_life_time)
        return response
    
class Log_in(APIView):

    def post(self, request):
        if "username" in request.data and request.data["username"]:
            username = request.data.get("username")
        elif "phone" in request.data and request.data["phone"]:
            username = get_object_or_404(User, phone=request.data.get("phone")).username
        else:
            return Response({"message": "Error in body"}, status=HTTP_400_BAD_REQUEST)
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            life_time = datetime.now() + timedelta(days=7)
            format_life_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
            response = Response({"user": UserSerializer(user).data})
            response.set_cookie(key="token", value=token.key, httponly=True, secure=True, samesite="Strict", expires=format_life_time)
            return response
        else:
            return Response({"message": "No user matching credentials"}, status=HTTP_404_NOT_FOUND)


class Log_out(APIView):
    authentication_classes = [HttpOnlyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        response = Response(status=HTTP_204_NO_CONTENT)
        response.delete_cookie("token", samesite="Strict")
        return response


class All_users(APIView):
    authentication_classes = [HttpOnlyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(User.objects.all(), many=True).data)


class A_user(APIView):
    authentication_classes = [HttpOnlyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, userid=None):
        if userid is not None:
            user = get_object_or_404(User, id = userid)
            return Response(UserSerializer(user).data)
        else:
            # Accessing your own info with "me" endpoint
            return Response(UserSerializer(request.user).data)

    def delete(self, request, userid=None):
        # Log user out and delete the user
        request.user.auth_token.delete()
        response = Response(status=HTTP_204_NO_CONTENT)
        response.delete_cookie("token")
        request.user.delete()
        return response
        

class Validate(APIView):
    authentication_classes = [HttpOnlyTokenAuthentication]
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        code = request.data["code"]
        message = request.user.check_code(code, False)
        return Response(
            {"message": message, "is_valid": message == "valid code"}
        )
 
   
class Resend(APIView):
    authentication_classes = [HttpOnlyTokenAuthentication]
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        try:
            request.user.send_text(False)
        except:
            return Response(
                {"message": "Error sending text. Try again."},
                status=HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Text sent!"}
        )


class InitiateReset(APIView):

    def post(self, request):
        user = get_object_or_404(User, phone=request.data["phone"])
        try:
            user.send_text(True)
        except:
            return Response(
                {"message": "Error sending text, try again"},
                status=HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Text sent!"}
        )
    
    
class ValidateReset(APIView):

    def post(self, request):
        user = get_object_or_404(User, phone=request.data['phone'])
        code = request.data['code']
        message = user.check_code(code, True)
        is_valid = message == "valid code"
        # With a valid code, reset password and un-validate password reset for the future
        if is_valid:
            user.set_password(request.data['password'])
            user.reset = ''
            user.save()
        return Response(
            {"message": message, "is_valid": is_valid}
        )
 