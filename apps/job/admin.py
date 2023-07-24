from django.contrib import admin

from apps.job.models import Job, JobApplied, Training, TrainingApplied, EmployerDetail


# Register your models here.
admin.site.register([
    Job
])

admin.site.register([
    JobApplied
])

admin.site.register([
    Training
])

admin.site.register([
    TrainingApplied
])

admin.site.register([
    EmployerDetail
])
