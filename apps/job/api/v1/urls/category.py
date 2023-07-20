from django.urls import path
from rest_framework import routers

from apps.job.api.v1.views import CategoryViewSet


router = routers.DefaultRouter()
router.register(r'', CategoryViewSet, basename='category')


urlpatterns = [
]

urlpatterns += router.urls
