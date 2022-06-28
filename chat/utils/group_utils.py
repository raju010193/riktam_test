from users.models import AppUser
from ..models import Groups, GroupChat, GroupMembers
from ..utils.base_utils import BaseUtils


class GroupUtils(BaseUtils):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group_obj = None
        self.status_code = 200
        # self.sender = kwargs.get('user')
        # self.group = None

    @staticmethod
    def get_group_member(**kwargs):
        """
        get group member
        """
        filter_data = {}
        if kwargs.get('member'):
            filter_data['member'] = kwargs.get('member')
        if kwargs.get('group'):
            filter_data['group'] = kwargs.get('group')
        if kwargs.get('group_id'):
            filter_data['group__uuid'] = kwargs.get('group_id')

        return GroupMembers.objects.filter(**filter_data)

    @staticmethod
    def get_user(user_uuid):
        """
        get user
        """
        return AppUser.objects.filter(uuid=user_uuid).first()

    def add_or_update_group_member(self, kwargs):
        """
        Add or update the group members
        """
        member = self.get_user(kwargs.get('member'))
        if member is None:
            self.status_code = 404
            return {
                'member': kwargs.get('member'),
                'message': 'member details not found'
            }
        member_obj = self.get_group_member(member=member, group=self.group).first()
        if member_obj:
            member_obj.is_mark_as_admin = kwargs.get('is_group_admin')
            member_obj.save()
            return {
                'message': 'Updated'
            }
        group_member = GroupMembers(member=member, group=self.group, added_by=self.sender,
                                    is_group_admin=kwargs.get('is_group_admin'))
        group_member.save()
        return {
            'message': 'Added'
        }

    def add_group_members(self, **kwargs):
        self.get_group(kwargs.get('group_id'))
        if self.group is None:
            return {
                       'message': 'group details not found'
                   }, 404
        errors = list(map(self.add_or_update_group_member, kwargs.get('users_list')))
        return errors, self.status_code

    def add_group(self, **kwargs):
        """
        Create or update group details
        """

        group_obj = Groups(name=kwargs.get('name'), group_info=kwargs.get('group_info'), created_by=self.sender)
        group_obj.save()
        self.group = group_obj
        # add created person as admin
        self.add_or_update_group_member({
            'is_group_admin': True,
            'member': self.sender.uuid
        })
        # self.group_obj = group_obj

    def update_group(self, **kwargs):
        group_obj = self.get_group(group_id=kwargs.get('group_id'))
        if group_obj is None:
            return {
                       'message': "group details not found"
                   }, 404
        group_obj.group_info = kwargs.get('group_info')
        group_obj.name = kwargs.get('name')
        group_obj.save()

    def delete_group(self, group_id):
        pass

    @staticmethod
    def get_groups(search_key=None):
        """
        Get all groups
        """
        filter_data = dict()
        if search_key:
            filter_data['name__icontains'] = search_key
        return Groups.objects.filter(**filter_data)

    @staticmethod
    def get_group_messages(group_id):
        """
        Get group messages
        """
        return GroupChat.objects.filter(receiver__uuid=group_id).order_by('created_at')

    def send_group_message(self, **kwargs):
        """
        Send message to group
        """
        self.get_group(group_id=kwargs.get('group_id'))
        if self.group is None:
            return {
                       'message': "group details not found"
                   }, 404
        GroupChat.objects.create(sender=self.sender, receiver=self.group, message=kwargs.get('message'))
        return {
                   'message': "Message sent successfully"
               }, 200
