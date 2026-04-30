from rest_framework import serializers
from .models import Users
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Users
        fields=[
            'id',
            'username',
            'password',
            'email',
            'role',
            'address'
        ]
        read_only_fields=["id"]
    def create(self, validated_data):
        password=validated_data.pop('password')
        user=Users(**validated_data)

        # user.set_password(password)

        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user

        return data
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = [
            'id',
            'username',
            'email',
            'role',
            'address'
        ]