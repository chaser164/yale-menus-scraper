from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
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
from utilities import HttpOnlyTokenAuthentication

from .models import User
from .serializers import UserSerializer


class Sign_up(APIView):
    
    def post(self, request):
        request.data["username"] = request.data["email"]
        # Add user attempt
        try:
            user = User.objects.create_user(**request.data)
        except:
            return Response({"message": "Email already in use"}, status=HTTP_400_BAD_REQUEST)
        # Send email attempt
        try:
            user.send_email(False)
        except:
            user.delete()
            return Response({"message": "Error sending email, try again"}, status=HTTP_400_BAD_REQUEST)
        token = Token.objects.create(user=user)
        life_time = datetime.now() + timedelta(days=7)
        format_life_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        response = Response({"user": UserSerializer(user).data})
        response.set_cookie(key="token", value=token.key, httponly=True, secure=True, samesite="None", expires=format_life_time)
        return response
    
class Log_in(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            life_time = datetime.now() + timedelta(days=7)
            format_life_time = life_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
            response = Response({"user": UserSerializer(user).data})
            response.set_cookie(key="token", value=token.key, httponly=True, secure=True, samesite="None", expires=format_life_time)
            return response
        else:
            return Response({"message": "No user matching credentials"}, status=HTTP_404_NOT_FOUND)


class Log_out(APIView):
    authentication_classes = [HttpOnlyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        response = Response(status=HTTP_204_NO_CONTENT)
        response.delete_cookie("token", samesite="None")
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
        request.user.auth_token.delete()
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
            request.user.send_email(False)
        except:
            return Response(
                {"message": "Error sending email. Try again."},
                status=HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Email sent!"}
        )


class InitiateReset(APIView):

    def post(self, request):
        user = get_object_or_404(User, email=request.data["email"])
        try:
            user.send_email(True)
        except:
            return Response(
                {"message": "Error sending email, try again"},
                status=HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "Email sent!"}
        )
    
    
class ValidateReset(APIView):

    def post(self, request):
        user = get_object_or_404(User, email=request.data['email'])
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
 