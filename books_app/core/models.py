from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.utils.translation import gettext_lazy as _

from books_app import settings


class UserManager(BaseUserManager):
    """Custom user manager that uses email as username"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class BookGender(models.Model):
    """Book gender model"""
    name = models.CharField(max_length=30)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True
    )
    class Meta:
        unique_together = (('user', 'name'),)


class Book(models.Model):
    """Model for book objects"""
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255)
    num_pages = models.IntegerField()

    class BookStatus(models.TextChoices):
        READING = 'READING', _('Reading')
        COMPLETED = 'COMPLETED', _('Completed')
        DROPPED = 'DROPPED', _('Dropped')
        PLAN_TO_READ = 'PLAN_TO_READ', _('Plan to read')

    status = models.CharField(
        max_length=15,
        choices=BookStatus.choices,
        default=BookStatus.READING,
    )

    score = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True
    )

    gender = models.ForeignKey(BookGender, on_delete=models.SET_NULL,
                               blank=True, null=True)

    class Meta:
        unique_together = (('user', 'title'),)


