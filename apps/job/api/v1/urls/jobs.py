from django.urls import path
from rest_framework import routers

from apps.job.api.v1.views import JobAppliedViewset, JobViewSet


router = routers.DefaultRouter()
router.register(r'apply', JobAppliedViewset, 'job_apply')
router.register(r'', JobViewSet, 'job')


urlpatterns = [
]

urlpatterns += router.urls
