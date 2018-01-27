"""
mangers for all the system
"""
from django.contrib.auth.models import BaseUserManager

from .querysets import AccountQueryMixin, AccountQuerySet


class UserManager(BaseUserManager, AccountQueryMixin):
    """ custom user managers """

    def get_queryset(self):
        return AccountQuerySet(self.model, using=self._db)

    def create_user(self, email, first_name, password, last_name=None):
        """create user method  """
        if not email:
            raise ValueError("ENTER AN EMAIL BUDDY")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, password, last_name=None):
        """ create super user """
        user = self.create_user(email, first_name, password, last_name)
        user.is_staff=True
        user.is_superuser = True
        user.save() 
        return user
