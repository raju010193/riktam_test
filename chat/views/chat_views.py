from django.shortcuts import render
from rest_framework import viewsets, generics, status
from riktam_test.response_util import response_format
from rest_framework.request import Request
from ..serializers.chat_serializer import ChatSerializer, ChatDataSerializer
from ..utils.chat_utils import ChatUtils
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import BasePermission, IsAuthenticated
from users.permissions import IsAdminAuthenticated

import logging

LOG = logging.getLogger(__name__)


class ChatAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer
    utility_class = ChatUtils

    def post(self, req: Request):
        """
        Add new Group Member
        """
        try:
            serializer_data = self.serializer_class(data=req.data)
            if serializer_data.is_valid() is False:
                return response_format(error=serializer_data.errors, is_success=False,
                                       status=status.HTTP_400_BAD_REQUEST)
            utility_obj = self.utility_class(user=req.user)
            message_dict, status_code = utility_obj.send_message(**serializer_data.validated_data)
            if status_code != 200:
                LOG.warning(message_dict.get('message'))
                return response_format(message=message_dict.get('message'), error='Not found', is_success=False,
                                       status=status.HTTP_404_NOT_FOUND)
            LOG.info('{0} Group added')
            return response_format(data=serializer_data.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, req: Request):
        """
        Get all Group members
        """
        try:

            receiver_id = req.GET.get('receiver_id')
            # user_model = get_user_model()
            data = self.utility_class(user=req.user).get_messages_by_user(receiver=receiver_id)
            ser_data = ChatDataSerializer(data, many=True).data
            LOG.info('fetching user details ')
            return response_format(data=ser_data, status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersViewsAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

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
