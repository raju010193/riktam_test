from rest_framework import serializers
# from users.models import AppUser
from django.contrib import auth
from users.models import User,AppUser
# from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class LoginSerializer(serializers.Serializer):
    # email = serializers.EmailField(max_length=255, min_length=3)
    username = serializers.CharField(
        max_length=255, min_length=3, write_only=True)
    password = serializers.CharField(
        max_length=68, write_only=True)

    token = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_token(self, obj):
        user = AppUser.objects.get(username=obj['username'])
        tokens = user.tokens()
        return {
            'refresh_token': tokens['refresh'],
            'access_token': tokens['access']
        }

    @staticmethod
    def get_user(obj):
        return {
            'username': obj.get('username'),
            'uuid': obj.get('uuid'),
            # 'group': obj.username,
        }



    class Meta:
        model = AppUser
        fields = ['email', 'password', 'username', 'tokens',]

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        # if not user.is_emailverified:
        #     raise AuthenticationFailed('User is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
            'uuid':user.uuid
        }

        return super().validate(attrs)


class RegisterSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=False,allow_null=True)
    first_name = serializers.CharField(max_length=50, required=True, trim_whitespace=True)
    last_name = serializers.CharField(max_length = 50, required=True, trim_whitespace=True)
    username = serializers.CharField(max_length=40, required=True, trim_whitespace=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8,required=False)
