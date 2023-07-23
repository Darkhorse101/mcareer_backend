

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.job.models import Category, Industry, Job, JobApplied, Training, TrainingApplied
from rest_framework import serializers

from apps.users.api.v1.serializers import UserDetailSerializer


class IndustrySerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Industry
        read_only_fields = ('created_at', 'id', 'slug')
        fields = (
            'id',
            'name',
            'created_at',
            'slug'
        )


class CategorySerializer(serializers.ModelSerializer):
    parent_category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Category
        read_only_fields = ('created_at', 'id', 'slug')
        fields = (
            'id',
            'name',
            'parent_category',
            'created_at',
            'slug'
        )


class JobSerializer(DynamicFieldsModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(
        queryset=Industry.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = Job
        read_only_fields = ('created_at', 'id', 'slug', 'created_by')
        fields = (
            'id',
            'title',
            'description',
            'expiry_date',
            'slug',
            'industry',
            'category'
        )


class TrainingSerializer(DynamicFieldsModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(
        queryset=Industry.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())

    class Meta:
        model = Training
        read_only_fields = ('created_at', 'id', 'slug', 'created_by')
        fields = (
            'id',
            'title',
            'description',
            'expiry_date',
            'slug',
            'industry',
            'category',
            'start_time',
            'end_time'
        )


class JobAppledSerializer(DynamicFieldsModelSerializer):
    job = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all()
    )

    class Meta:
        model = JobApplied
        read_only_fields = ('id', 'jobseeker')
        fields = (
            'id',
            'job',
            'applied_statues'
        )

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.upper() == 'GET':
            fields['jobseeker'] = UserDetailSerializer(
                fields=(
                    'id', 'full_name', 'email'
                )
            )
        return fields
    

class TrainingAppledSerializer(DynamicFieldsModelSerializer):
    job = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all()
    )

    class Meta:
        model = TrainingApplied
        read_only_fields = ('id', 'jobseeker')
        fields = (
            'id',
            'job',
            'jobseeker',
            'applied_statues'
        )

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.upper() == 'GET':
            fields['jobseeker'] = UserDetailSerializer(
                fields=(
                    'id', 'full_name', 'email'
                )
            )
        return fields