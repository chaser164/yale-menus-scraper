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
        # Add user attempt
        try:
            user = User.objects.create_user(**request.data)
        except:
            return Response({"message": "Email already in use"}, status=HTTP_400_BAD_REQUEST)
        # Send email attempt
        try:
            user.send_verification_email()
        except:
            return Response({"message": "Error sending email"}, staut=HTTP_400_BAD_REQUEST)
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
            return Response({"message": "No user matching credentials"}, status=HTTP_404_NOT_FOUND)


class Log_out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class All_users(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(User.objects.all(), many=True).data)


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
        
    def delete(self, request, userid=None):
        request.user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
        

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
        try:
            request.user.send_verification_email()
        except:
            return Response(
                {"message": "Error sending email"}
            )
        return Response(
            {"message": "Email sent!"}
        )