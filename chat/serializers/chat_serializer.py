from rest_framework import serializers
from ..models import Chat


class ChatSerializer(serializers.Serializer):
    receiver_id = serializers.UUIDField(required=True)
    message = serializers.CharField(required=True, trim_whitespace=True)


class ChatDataSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('uuid', 'sender', 'receiver', 'message','created_at')

    @staticmethod
    def fetch_details(obj):
        return {
            'uuid': obj.uuid,
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name
        }

    def get_sender(self, obj):
        return self.fetch_details(obj.sender)

    def get_receiver(self, obj):
        return self.fetch_details(obj.receiver)
