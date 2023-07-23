from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.core.viewsets import CreateListUpdateDestroyViewSet, CreateListUpdateViewSet
from apps.job.api.v1.serializer import CategorySerializer, IndustrySerializer, JobAppledSerializer, JobSerializer, TrainingSerializer
from apps.job.models import Category, Industry, Job, JobApplied, Training


class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class JobViewSet(CreateListUpdateDestroyViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
        )


class JobAppliedViewset(CreateListUpdateViewSet):
    queryset = JobApplied.objects.all()
    serializer_class = JobAppledSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print('o')
        serializer.save(
            jobseeker=self.request.user
        )
        return super().perform_create(serializer)


class TrainingViewSet(CreateListUpdateDestroyViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
        )
