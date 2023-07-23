from rest_framework import routers

from apps.job.api.v1.views import TrainingAppliedViewset, TrainingViewSet



router = routers.DefaultRouter()
router.register(r'apply', TrainingAppliedViewset, basename='training_applied')
router.register(r'', TrainingViewSet, basename='training')


urlpatterns = [
]

urlpatterns += router.urls
