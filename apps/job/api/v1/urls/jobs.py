from django.urls import path
from rest_framework import routers

from apps.job.api.v1.views import JobViewSet



app_name = 'job'

router = routers.DefaultRouter()
router.register(r'', JobViewSet, basename='job')


urlpatterns = [
]

urlpatterns += router.urls
