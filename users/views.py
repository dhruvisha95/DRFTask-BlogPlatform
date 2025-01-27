from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.serializers import LoginSerializer, RegisterSerializer

# Create your views here.
class RegisterAPI(APIView): 
    """
    API endpoint that allows users to register.
    Methods
    -------
    post(request):
        If the data is valid, saves the new user and returns a success message.
        If the data is invalid, returns the validation errors.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : "Registration successfull"} ,serializer.data, status=status.HTTP_200_OK)
        return Response({'error' : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPI(APIView): 
    """
    LoginAPI class handles user login requests.
    Methods:
        post(request):
            Returns a success message and user details if authentication is successful.
            Returns an error message if authentication fails.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({'error' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email = serializer.data['email'] , password = serializer.data['password'])
        token, _ = Token.objects.get_or_create(user = user)
        user = Token.objects.get(key=token.key)
        return Response({'message' : "Login successfull"}, user, status=status.HTTP_200_OK)
