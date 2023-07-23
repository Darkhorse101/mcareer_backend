from rest_framework import routers

from apps.job.api.v1.views import TrainingViewSet



router = routers.DefaultRouter()
router.register(r'', TrainingViewSet, basename='training')


urlpatterns = [
]

urlpatterns += router.urls
