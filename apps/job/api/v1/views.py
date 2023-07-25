from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewsets import CreateListUpdateDestroyViewSet, CreateListUpdateViewSet
from apps.job.api.v1.serializer import CategorySerializer, IndustrySerializer, JobAppledSerializer, JobSerializer, TrainingAppledSerializer, TrainingSerializer
from apps.job.models import Category, Industry, Job, JobApplied, Training, TrainingApplied
from apps.job.utils import compute_similarity



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

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='recommendation',
    )
    def recommendation_job(self, request, *args, **kwargs):
        qs = self.get_queryset()
        user_skills = [skill.name for skill in request.user.skills.all()]
        query_result = qs
        if user_skills:
            query_result = query_result.annotate(distance=compute_similarity("description", user_skills))
            query_result = query_result.filter(distance__lte=0.7).order_by("-distance")
        else:
            query_result = []
       
        serializer = serializer = self.get_serializer(query_result, many=True)
        return Response(serializer.data)


class JobAppliedViewset(CreateListUpdateViewSet):
    queryset = JobApplied.objects.all()
    serializer_class = JobAppledSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            jobseeker=self.request.user
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
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
    serializer_class = TrainingAppledSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            jobseeker=self.request.user
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='me',
    )
    def training_apply_by_me(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(jobseeker=request.user)
        serializer = serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
