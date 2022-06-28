from django.db import models
from users.models import AppUser
import uuid


# Create your models here.
# class Members(models.Model):
#     """
#     Group Members
#     """
#     uuid = models.UUIDField(unique=True, default=uuid.uuid4)
#     user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='group_user')
#     added_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='group_user_added_by')
#     # group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='member_related_group')
#     added_at = models.DateTimeField(auto_created=True)
#     is_group_admin = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"{self.uuid}"
#
#     class Meta:
#         verbose_name = 'Group Members'
#         verbose_name_plural = 'Group Members'
#         db_table = 'group_members'
#         indexes = [
#             models.Index(fields=["uuid"]),
#             models.Index(fields=["group"]),
#         ]


class Groups(models.Model):
    """
    Groups
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=240, default=None)
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='group_created_by')
    created_at = models.DateTimeField(auto_now=True)
    group_info = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = 'Groups'
        verbose_name_plural = 'Groups'
        db_table = 'groups'
        indexes = [
            models.Index(fields=["uuid"]),
            models.Index(fields=["created_by"]),
        ]


class GroupMembers(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='group')
    member = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="all_groups")
    is_group_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='group_user_added_by')

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = 'Group Members'
        verbose_name_plural = 'Group Members'
        db_table = 'group_members'
        indexes = [
            models.Index(fields=["uuid"]),
            models.Index(fields=["group"]),
            models.Index(fields=["member"]),
        ]


class Chat(models.Model):
    """
    Chat
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='receive')
    message = models.TextField()
    last_seen = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chat'
        db_table = 'chat'
        indexes = [
            models.Index(fields=["uuid"]),
            models.Index(fields=["sender"]),
            models.Index(fields=["receiver"]),
        ]


class GroupChat(models.Model):
    """
    Group Chat
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='group_sender')
    receiver = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='group_receiver')
    message = models.TextField()
    last_seen = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = 'Group Chat'
        verbose_name_plural = 'Group Chat'
        db_table = 'group chat'
        indexes = [
            models.Index(fields=["uuid"]),
            models.Index(fields=["sender"]),
            models.Index(fields=["receiver"]),
        ]
