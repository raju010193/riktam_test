from users.models import AppUser
from ..models import Chat
from ..utils.base_utils import BaseUtils


class ChatUtils(BaseUtils):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group_obj = None
        # self.sender = kwargs.get('user')
        # self.group = None

    def get_messages_by_user(self, receiver):

        return Chat.objects.filter(sender=self.sender, receiver__uuid=receiver).order_by('created_at')

    def send_message(self, **kwargs):
        receiver_obj = self.get_receiver(kwargs.get('receiver_id'))
        if receiver_obj is None:
            return {
                       'message': "Receiver details not found"
                   }, 404
        Chat.objects.create(sender=self.sender, receiver=receiver_obj, message=kwargs.get('message'))
        return {
                   'message': "Message sent successfully"
               }, 200
