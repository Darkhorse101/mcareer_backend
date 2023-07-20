

from apps.core.serializers import DynamicFieldsModelSerializer
from apps.job.models import Category, Industry, Job
from apps.users.api.v1.serializers import UserDetailSerializer
from rest_framework import serializers


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
    parent_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)


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
