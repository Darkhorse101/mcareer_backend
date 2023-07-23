from django.db import models

from apps.core.models import BaseModel, SlugModel
from django.contrib.auth import get_user_model

USER = get_user_model()

# Choices for applied_statues field
APPLIED = 'Applied'
SELECTED = 'Selected'
REJECTED = 'Rejected'
APPLIED_STATUSES_CHOICES = [
    (APPLIED, 'Applied'),
    (SELECTED, 'Selected'),
    (REJECTED, 'Rejected'),
]


class Industry(BaseModel, SlugModel):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)


class Category(BaseModel, SlugModel):
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.name)


# Create your models here.
class Job(BaseModel, SlugModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    expiry_date = models.DateTimeField()
    industry = models.ForeignKey(
        Industry, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(USER, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['industry']),
            models.Index(fields=['category']),
        ]

    def __str__(self) -> str:
        return str(self.title)


class Training(BaseModel, SlugModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    expiry_date = models.DateTimeField()
    industry = models.ForeignKey(
        Industry, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(USER, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['industry']),
            models.Index(fields=['category']),
        ]

    def __str__(self) -> str:
        return str(self.title)


class JobApplied(BaseModel):
    jobseeker = models.ForeignKey(USER, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='job_applications')
    applied_statues = models.CharField(
        choices=APPLIED_STATUSES_CHOICES, max_length=50, default=APPLIED)

    def __str__(self) -> str:
        return f'Applied By {self.jobseeker} in {self.job} Job'


class TrainingApplied(BaseModel):
    jobseeker = models.ForeignKey(USER, on_delete=models.CASCADE)
    training = models.ForeignKey(
        Training, on_delete=models.CASCADE, related_name='training_applications')
    applied_statues = models.CharField(
        choices=APPLIED_STATUSES_CHOICES, max_length=50, default=APPLIED)
    

    def __str__(self) -> str:
        return f'Applied By {self.jobseeker} in {self.training} Training'


class EmployerDetail(models.Model):
    owner = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name='employer')
    company_name = models.CharField(max_length=50)
    pan_vat = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    industry = models.ForeignKey(
        Industry, on_delete=models.SET_NULL, null=True)
