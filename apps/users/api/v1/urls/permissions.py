from django.urls import path
from rest_framework import routers

from apps.users.api.v1.permissions import GroupViewSet, UserPermissionView


router = routers.DefaultRouter()
router.register(r'group', GroupViewSet, basename='group')


urlpatterns = [
    path('assign-permissions/', UserPermissionView.as_view(), name='assign_permissions'),
]
    
urlpatterns += router.urls


