from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from estates.models import Estate
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    phone = models.CharField('phone', max_length=50)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)
    created_at = models.DateTimeField('date created', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_owner = models.BooleanField('is owner', default=True)
    is_security = models.BooleanField('is security', default=False)
    is_resident = models.BooleanField('is resident', default=False)
    estate = models.ForeignKey(Estate, on_delete=models.SET_NULL, related_name='people', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        unique_together = ('phone', 'estate',)

    @property
    def role(self):
        if self.is_owner:
            return 'admin'
        if self.is_security:
            return 'security'
        if self.is_resident:
            return 'resident'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email='info@gateplus.dev', **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject=subject, message=message, from_email=from_email)
