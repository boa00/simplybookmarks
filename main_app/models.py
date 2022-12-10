from datetime import datetime, timedelta
import jwt

from django.db import models
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class UserManager(BaseUserManager):
    
    def create_user(self, email, password):
        if email is None:
            raise TypeError("User must have an email")

        if password is None:
            raise TypeError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    email = models.EmailField(db_index=True, unique=True)
    activated = models.BooleanField(default=False)
    alive = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    @property
    def token(self):
        return self._generate_jwt_token()
