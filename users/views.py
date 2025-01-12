from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.serializers import LoginSerializer, RegisterSerializer

# Create your views here.
class RegisterAPI(APIView): 
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPI(APIView): 
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        
        user = authenticate(email = serializer.data['email'] , password = serializer.data['password'])
        token, _ = Token.objects.get_or_create(user = user)
        return Response(serializer.validated_data,status=status.HTTP_200_OK)
