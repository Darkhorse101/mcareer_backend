from django.db import models

from apps.core.models import BaseModel, SlugModel
from django.contrib.auth import get_user_model

USER = get_user_model()

class Industry(BaseModel, SlugModel):
    name = models.CharField(max_length=50)

class Category(BaseModel, SlugModel):
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)


# Create your models here.
class Job(BaseModel, SlugModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    expiry_date = models.DateTimeField()
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(USER, on_delete=models.CASCADE)


    class Meta:
        indexes = [
            models.Index(fields=['industry']),
            models.Index(fields=['category']),
        ]