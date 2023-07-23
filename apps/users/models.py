import os

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from apps.core.constants import CATALOG_DISPLAY_MODE, LIST_VIEW
from apps.core.models import BaseModel, SlugModel
from apps.core.utils.helpers import get_upload_path, get_uuid_filename
from apps.core.validators import validate_phone_number

from apps.users.manager import UserManager


USER_TYPE = [('Employer', 'employer'), ('Jobseeker', 'Jobseeker')]
class User(AbstractUser, BaseModel):
    
    
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )

    full_name = models.CharField(
        _('full name'),
        max_length=150,
        blank=True, null=True
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        }
    )

    # Below fields are optional
    profile_picture = models.ImageField(
        upload_to=get_upload_path,
        blank=True
    )

    phone_number = models.CharField(
        _('phone number'),
        null=True,
        validators=[validate_phone_number],
        max_length=25,
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },
        unique=True
    )
    digit_validator = RegexValidator(r'^\d{6}$', 'Enter a valid 6-digit number.')
    verification_code = models.IntegerField(null=True, validators=[
        MinValueValidator(100000),
        MaxValueValidator(999999),
        digit_validator
    ])

    is_verified = models.BooleanField(default=False)
    
    user_type = models.CharField(choices=USER_TYPE, max_length=25, null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name or self.email
    


class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    start_year = models.DateField()
    end_year = models.DateField()
    is_currently_working = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='media/certificate', null=True, blank=True)

    def __str__(self) -> str:
        return f'Work Experience of {self.user}'


