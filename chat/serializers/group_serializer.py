from rest_framework import serializers
from django.db.models import F


class CreateGroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True, trim_whitespace=True)
    group_info = serializers.CharField(required=False, trim_whitespace=True, allow_blank=True, allow_null=True)


class GroupMemberSerializer(serializers.Serializer):
    member = serializers.UUIDField(required=True)
    is_group_admin = serializers.BooleanField(default=False)


class AddGroupMembersSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(required=True)
    users_list = serializers.ListSerializer(child=GroupMemberSerializer(), required=True)


class GroupChatSerializer(serializers.Serializer):
    group_id = serializers.UUIDField(required=True)
    message = serializers.CharField(required=True, trim_whitespace=True)


class GroupMemberDataSerializer(serializers.Serializer):
    group = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()
    added_at = serializers.SerializerMethodField()

    @staticmethod
    def get_group(obj):
        return {
            'name': obj.group.name,
            'uid': obj.group.uuid
        }

    @staticmethod
    def get_member(obj):
        return {
            'uuid': obj.member.uuid,
            'first_name': obj.member.first_name,
            'last_name': obj.member.last_name,
            'username': obj.member.username
        }

    @staticmethod
    def get_added_at(obj):
        return obj.created_at


class GroupChatDataSerializer(serializers.Serializer):
    group = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    posted_at = serializers.SerializerMethodField()

    @staticmethod
    def get_message(obj):
        return obj.message

    @staticmethod
    def get_group(obj):
        return {
            'name': obj.receiver.name,
            'uuid': obj.receiver.uuid,
            'members': obj.receiver.group.values(first_name=F('member__first_name'), last_name=F('member__last_name'),
                                                 user_id=F('member__uuid'), username=F('member__username'))
        }

    @staticmethod
    def get_sender(obj):
        return {
            'uuid': obj.sender.uuid,
            'first_name': obj.sender.first_name,
            'last_name': obj.sender.last_name,
            'username': obj.sender.username
        }

    @staticmethod
    def get_posted_at(obj):
        return obj.created_at
