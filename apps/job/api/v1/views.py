from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewsets import CreateListUpdateDestroyViewSet, CreateListUpdateViewSet
from apps.job.api.v1.serializer import CategorySerializer, IndustrySerializer, JobAppledSerializer, JobSerializer, TrainingSerializer
from apps.job.models import Category, Industry, Job, JobApplied, Training, TrainingApplied


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
        serializer.save(
            jobseeker=self.request.user
        )
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path='me',
    )
    def job_apply_by_me(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(jobseeker=request.user)
        serializer = serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)



class TrainingViewSet(CreateListUpdateDestroyViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
        )


class TrainingAppliedViewset(CreateListUpdateViewSet):
    queryset = TrainingApplied.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            jobseeker=self.request.user
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path='me',
    )
    def training_apply_by_me(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(jobseeker=request.user)
        serializer = serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
