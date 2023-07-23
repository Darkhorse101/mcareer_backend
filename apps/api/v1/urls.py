from django.urls import path, include

app_name = "api_v1"

urlpatterns = [
    path('user/', include('apps.users.api.v1.urls.users')),
    path('permissions/', include('apps.users.api.v1.urls.permissions')),
    path('job/', include('apps.job.api.v1.urls.jobs')),
    path('industry/', include('apps.job.api.v1.urls.industry')),
    path('category/', include('apps.job.api.v1.urls.category')),
    path('training/', include('apps.job.api.v1.urls.training')),
]
