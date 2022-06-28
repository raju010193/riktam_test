from django.shortcuts import render
from rest_framework import viewsets, generics, status
from riktam_test.response_util import response_format
from rest_framework.request import Request
from ..utils.group_utils import GroupUtils
from ..serializers.group_serializer import (CreateGroupSerializer, AddGroupMembersSerializer, GroupChatSerializer,
                                            GroupMemberDataSerializer, GroupChatDataSerializer)
from rest_framework.permissions import BasePermission, IsAuthenticated
from users.permissions import IsAdminAuthenticated

import logging

LOG = logging.getLogger(__name__)


class GroupAPI(generics.GenericAPIView):
    permission_classes = [IsAdminAuthenticated]
    serializer_class = CreateGroupSerializer
    utility_class = GroupUtils

    def post(self, req: Request):
        """
        Add new Group
        """
        try:
            serializer_data = self.serializer_class(data=req.data)
            if serializer_data.is_valid() is False:
                return response_format(error=serializer_data.errors, is_success=False,
                                       status=status.HTTP_400_BAD_REQUEST)
            utility_obj = self.utility_class(user=req.user)
            utility_obj.add_group(**serializer_data.validated_data)
            LOG.info('{0} Group added')
            return response_format(data=serializer_data.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, req: Request):
        """
        Get all Groups
        """
        try:

            # username = req.GET.get('username')
            # user_model = get_user_model()
            data = self.utility_class(user=req.user).get_groups().values('uuid', 'name',
                                                                         'group_info',
                                                                         )
            LOG.info('fetching user details ')
            return response_format(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, req: Request):
        """
        update group
        """
        try:
            serializer_data = self.serializer_class(data=req.data)
            if serializer_data.is_valid() is False:
                return response_format(error=serializer_data.errors, is_success=False,
                                       status=status.HTTP_400_BAD_REQUEST)
            utility_obj = self.utility_class(user=req.user)
            utility_obj.update_group(**serializer_data.validated_data)
            LOG.info('{0} Group added')
            return response_format(data=serializer_data.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, req: Request):
        """
        Delete Group
        """
        try:

            group_id = req.GET.get('group_id')
            # user_model = get_user_model()
            self.utility_class(user=req.user).delete_group(group_id=group_id)
            return response_format(message="User deleted successfully!", status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupMembersAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddGroupMembersSerializer
    utility_class = GroupUtils

    def post(self, req: Request):
        """
        Add new Group Member
        Body: {
                "group_id":"d7cc88ab-ac50-420e-8f7c-c2e4cf4ed899",
                "users_list":[{
                "member":"abb1133f-58c3-4fee-ad30-e28836a313f1",
                "is_mark_group_admin":false
                }
                ]
                }
        """
        try:
            serializer_data = self.serializer_class(data=req.data)
            if serializer_data.is_valid() is False:
                return response_format(error=serializer_data.errors, is_success=False,
                                       status=status.HTTP_400_BAD_REQUEST)
            utility_obj = self.utility_class(user=req.user)
            message_dict, status_code = utility_obj.add_group_members(**serializer_data.validated_data)
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

            group_id = req.GET.get('group_id')
            # user_model = get_user_model()
            data = self.utility_class(user=req.user).get_group_member(group_id=group_id)
            ser_data = GroupMemberDataSerializer(data, many=True).data
            LOG.info('fetching user details ')
            return response_format(data=ser_data, status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, req: Request):
        """
        update group Member
        """
        try:
            serializer_data = self.serializer_class(data=req.data)
            if serializer_data.is_valid() is False:
                return response_format(error=serializer_data.errors, is_success=False,
                                       status=status.HTTP_400_BAD_REQUEST)
            utility_obj = self.utility_class(user=req.user)
            message_dict, status_code = utility_obj.add_group_members(**serializer_data.validated_data)
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

    def delete(self, req: Request):
        """
        Delete Group Memeber
        """
        try:

            group_id = req.GET.get('group_id')
            username = req.GET.get('username')
            # user_model = get_user_model()
            # self.utility_class(user=req.user).rem(group_id=group_id)
            return response_format(message="User deleted successfully!", status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupChatAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupChatSerializer
    utility_class = GroupUtils

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
            message_dict, status_code = utility_obj.send_group_message(**serializer_data.validated_data)
            if status_code != 200:
                LOG.warning(message_dict.get('message'))
                return response_format(message=message_dict.get('message'), error='Not found', is_success=False,
                                       status=status.HTTP_404_NOT_FOUND)
            LOG.info('{0} group message sent')
            return response_format(message=message_dict.get('message'), status=status.HTTP_201_CREATED)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, req: Request):
        """
        Get all Group members
        """
        try:

            group_id = req.GET.get('group_id')
            # user_model = get_user_model()
            data = self.utility_class(user=req.user).get_group_messages(group_id=group_id)
            ser_data = GroupChatDataSerializer(data,many=True).data
            LOG.info('fetching user details ')
            return response_format(data=ser_data, status=status.HTTP_200_OK)
        except Exception as e:
            LOG.error(e, exc_info=True)
            return response_format(error='Internal server error', message='server error',
                                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)
