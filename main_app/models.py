from django.db import models
from django.db.models import Q
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
    access_token = models.TextField(null=True, default=None) # used to get the connection to OpenID, should be hashed
    activated = models.BooleanField(default=False)
    alive = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('name', 'user'),)
    

class BookmarkQuerySet(models.QuerySet):
    def search(self, query):
        if query and query != "null":
            lookups = Q(title__icontains=query) | Q(description__icontains=query)
            return self.filter(lookups)
        return self

    def filter_user(self, user):
        return self.filter(user=user)

    def filter_tags(self, tag):
        if tag and tag != "All":
            if tag == "Untagged":
                return self.filter(tags__isnull=True)
            else:
                return self.filter(tags__name__contains=tag)
        return self

    def sort(self, order):
        sort_by = "created" if order == "asc" else "-created"
        return self.order_by(sort_by)


class BookmarkManager(models.Manager):
    def get_queryset(self):
        return BookmarkQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)

    def filter_user(self, user):
        return self.get_queryset().filter_user(user=user)

    def filter_tags(self, tag):
        return self.get_queryset().filter_tags(tag=tag)

    def sort(self, order):
        return self.get_queryset().sort(order=order)

        
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    title = models.CharField(max_length=300)
    link = models.TextField(null=False)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = BookmarkManager()
