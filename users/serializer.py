
from django.forms import ValidationError
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

from users.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'title', 'description', 'email', 'password', 'language', 'location')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=68, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        username = obj.get('username')
        tokens = User.objects.get(username=username).tokens
        return tokens

    class Meta:
        model = User
        fields = ('username', 'tokens', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed({
                'message': 'Username or password is not correct'
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'message': 'Account disabled'
            })

        data = {
            'username': user.username,
        }
        return data




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6, max_length=50, error_messages={
        "min_length": "Password must be more than 6 characters",
        "max_length": "Password should be less than 50 characters"
    })
    confirm_password = serializers.CharField(required=True, min_length=6, max_length=50, error_messages={
        "min_length": "Password must be more than 6 characters",
        "max_length": "Password should be less than 50 characters"
    })

    def validate(self, data):
        errors = {}

        if not self.context['request'].user.check_password(data.get('old_password')):
            errors['old_password'] = "Password was incorrected."
        
        if data.get('new_password') != data.get('confirm_password'):
            errors['confirm_password'] = "Passwords must be same"

        if data.get('new_password') == data.get('old_password'):
            errors['new_password'] = "Your new password is same with your old password"

        if errors:
            raise serializers.ValidationError(errors)

        return data

class UserEditSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'title', 'language', 'location', 'password',  'avatar', 'description']


class UserSerializer(serializers.ModelSerializer):
    # image_url = serializers.SerializerMethodField(method_name='get_image_url')

    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'title', 'language', 'location','password','email', 'avatar', 'description']


    # def get_image_url(self, obj):
    #     request = self.context.get('request')
    #     image_url = obj.image.url
    #     return request.build_absolute_uri(image_url)

