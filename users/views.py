from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from riktam_test.response_util import response_format
from rest_framework.request import Request
from .serializer import LoginSerializer, RegisterSerializer, AppUser
from rest_framework.permissions import BasePermission, IsAuthenticated
from .permissions import IsAdminAuthenticated
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate

import logging

LOG = logging.getLogger(__name__)


# Create your views here.

class LoginAPI(generics.GenericAPIView):
    """
    Login API
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Login user
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response_format(data=serializer.data, status=status.HTTP_200_OK)


class RegisterAPI(generics.GenericAPIView):
    """
    Manage users API
    """

    permission_classes = [IsAdminAuthenticated]
    serializer_class = RegisterSerializer

    def post(self, req: Request):
        """
        Add new user
        """
        try:
            serializer_data = self.serializer_class(data=req.data)
            if serializer_data.is_valid() is False:
                return response_format(error=serializer_data.errors, is_success=False,
                                       status=status.HTTP_400_BAD_REQUEST)
            user_model = get_user_model()
            new_user = user_model.objects.create_user_custom(
                serializer_data.validated_data.get("email").lower(),
                serializer_data.validated_data.get("password"),
                serializer_data.validated_data.get("first_name"),
                serializer_data.validated_data.get("last_name"),
                serializer_data.validated_data.get("username"),
                True,
                False
            )
            if isinstance(new_user, IntegrityError):
                LOG.warning('{0} user registration failed '.format(new_user.username))
                return response_format(error=STATUS_MESSAGES.get('STATUS_207'), is_success=False,
                                       message=MESSAGES.get('EMAIL_OR_MOBILE_EXISTS'),
                                       status=status.HTTP_207_MULTI_STATUS)
            LOG.info('{0} user registered '.format(new_user.username))
            return response_format(data=serializer_data.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, req: Request):
        """
        Get all users
        """
        try:

            username = req.GET.get('username')
            user_model = get_user_model()
            filter_data = dict()
            if username:
                filter_data['username'] = username
            data = user_model.objects.filter(**filter_data).exclude(username=req.user.username).values('uuid',
                                                                                                       'first_name',
                                                                                                       'last_name',
                                                                                                       'email',
                                                                                                       'username')
            if username:
                data = data.first()
            LOG.info('fetching user details ')
            return response_format(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, req: Request):
        """
        update user
        """
        try:
            serializer_data = self.serializer_class(data=req.data)
            if serializer_data.is_valid() is False:
                return response_format(error=serializer_data.errors, is_success=False,
                                       status=status.HTTP_400_BAD_REQUEST)

            user_model = get_user_model()
            try:
                user = user_model.objects.get(uuid=serializer_data.validated_data.get("uuid"))
                user.email = serializer_data.validated_data.get("email").lower()
                user.first_name = serializer_data.validated_data.get("first_name")
                user.last_name = serializer_data.validated_data.get("last_name")
                user.save()
            except Exception as e:
                LOG.error(e, exc_info=True)
                return response_format(error="User details not found", is_success=False,
                                       status=status.HTTP_204_NO_CONTENT)
            LOG.info('{0} user registered ')
            return response_format(data=serializer_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, req: Request):
        """
        Delete User
        ?uuid=user_uuid
        """
        try:

            user_uuid = req.GET.get('uuid')
            user_model = get_user_model()
            data = user_model.objects.filter(uuid=user_uuid).first()
            if data:
                data.delete()
                LOG.info('{0} user deleted '.format(user_uuid))
            return response_format(message="User deleted successfully!", status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)