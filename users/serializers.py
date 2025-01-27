from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['password', 'email', 'name', 'bio', 'picture', 'phone_number']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(name = validated_data.get('name') , 
                                              email = validated_data['email'],
                                              password = validated_data['password'],
                                              phone_number = validated_data.get('phone_number'),
                                              picture = validated_data.get('picture'),
                                              bio = validated_data.get('bio')
                                            )
        return user
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()    
    password = serializers.CharField()


class CustomUserSerialzer(serializers.ModelSerializer):
    email = serializers.EmailField()   
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'bio', 'picture', 'phone_number']
