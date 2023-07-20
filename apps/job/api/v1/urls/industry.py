from django.urls import path
from rest_framework import routers

from apps.job.api.v1.views import IndustryViewSet


router = routers.DefaultRouter()
router.register(r'', IndustryViewSet, basename='industry')


urlpatterns = [
]

urlpatterns += router.urls
