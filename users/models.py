from django.db import models
from django.contrib.auth.models import BaseUserManager, UserManager,AbstractBaseUser,PermissionsMixin,User
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth import models as auth_models
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
# Create your models here.


class CustomUserManager(UserManager, BaseUserManager):

    @staticmethod
    def is_user_exists(email, mobile):
        e_mail = None
        users = AppUser.objects.all()
        if email != '' and email is not None:
            user = users.filter(email=email).first()
            return user
        return users.filter(mobile=mobile).first()

    def create_user_custom(self, email, password, first_name, last_name, username, is_active=True, is_staff=False):
        try:
            user = self.model(
                email=CustomUserManager.normalize_email(email),
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_active=is_active,

            )
            user.set_password(password)
            user.save()
            return user
        except IntegrityError as e:
            return e


class AppUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    username = models.CharField(max_length=25, unique=True, db_index=True)
    email = models.EmailField(max_length=250, unique=False, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), blank=True, default=timezone.now)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False
    )
    is_active = models.BooleanField(
        _('active'),
        default=True
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    USERNAME_FIELD = 'username'
    # history = AuditlogHistoryField(db_index=True)
    objects = CustomUserManager()

    def get_short_name(self):
        return self.first_name

    @classmethod
    def get_user_object(cls, username):
        user_obj = AppUser.objects.get(username=username)
        return user_obj

    @classmethod
    def get_user_object_by_mobile(cls, username):
        user_obj = AppUser.objects.filter(username=username).first()
        return user_obj
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)

        }

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=["username"]),
        ]

    # def save(self, *args, **kwargs):
    #     if not self.role:
    #         roles = Roles.objects.filter(role_type=settings.ROLES.get('GENERAL'), is_active=True).first()
    #         self.role = roles
    #     super().save(*args, **kwargs)


auth_models.User = AppUser
