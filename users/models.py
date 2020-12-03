from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    username = models.CharField(_('Nom d\'utilisateur'),
                                max_length=128,
                                validators=[UnicodeUsernameValidator()])
    email = models.EmailField(_('Adresse électronique'),
                              max_length=256,
                              unique=True)

    # Is User a citizen of this town
    is_citizen = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username