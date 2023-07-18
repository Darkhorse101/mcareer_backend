# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from drf_yasg.utils import swagger_auto_schema
from apps.core.viewsets import CreateListUpdateDestroyViewSet
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from apps.users.api.v1.serializers import GroupSerializer, PermissionSerializer, UserPermissionSerializer

class UserPermissionView(APIView):
    serializer_class = UserPermissionSerializer

    def get(self, *args, **kwargs):
        qs = Permission.objects.all()
        serializer =  PermissionSerializer(qs, many=True)

        return Response(serializer.data, status=200)

    @swagger_auto_schema(request_body=UserPermissionSerializer)
    def post(self, request):
        serializer = UserPermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user_id'] # type: ignore
        permission_codenames = serializer.validated_data['permission_codenames'] # type: ignore

        # Assign permissions to the user
        user.user_permissions.set(Permission.objects.filter(codename__in=permission_codenames))

        return Response({"message": "Permissions assigned successfully"})
    

class GroupViewSet(CreateListUpdateDestroyViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, ]
    search_fields = ['name']

    
    

