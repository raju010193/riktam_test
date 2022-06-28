from users.models import AppUser
from ..models import Groups


class BaseUtils(object):
    def __init__(self, **kwargs):
        self.sender = kwargs.get('user')
        self.group = None

    @staticmethod
    def get_receiver(receiver_id):
        return AppUser.objects.filter(uuid=receiver_id).first()

    def get_group(self, group_id):
        self.group = Groups.objects.filter(uuid=group_id).first()

    def get_sender_group(self):
        return self.group.member_related_group.filter(user=self.sender).first()
