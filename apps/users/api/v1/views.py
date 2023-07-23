from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.core.viewsets import CreateListUpdateDestroyViewSet
from apps.users.api.v1.serializers import (
    UserDetailSerializer,
    CustomTokenObtainPairSerializer, PasswordChangeSerializer,
    UserRegistrationSerializer,
    UserVerificationSerializer
)
from django.contrib.auth.hashers import make_password
from apps.users.utils import generate_random_digits, send_forgor_password_email, send_verification_email

USER = get_user_model()


class CustomTokenViewBase(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserViewSet(CreateListUpdateDestroyViewSet):
    serializer_class = UserDetailSerializer
    queryset = USER.objects.filter(is_active=True)
    permission_class_mapper = {
        'create': []
    }
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = ['full_name', 'email', 'phone_number']
    filter_fields = ['is_staff', ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['put', ],
        serializer_class=PasswordChangeSerializer,
        permission_classes=[IsAuthenticated],
        url_name='change-password',
        url_path='password_change'
    )
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password1')
        user.set_password(password)
        user.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['patch'],
        url_name='register-user',
        permission_classes=[AllowAny],
        url_path='register',
        serializer_class=UserRegistrationSerializer,
    )
    def register(self, request, *args, **kwargs):
        email = request.data.get('email')
        full_name = request.data.get('full_name')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        user_type = request.data.get('user_type')

        existing_user = USER.objects.filter(email=email).first()
        if existing_user:
            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if not email or not password or not password2:
            return Response({'error': 'Email, password, and password2 are required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(
            UserRegistrationSerializer, data=request.data)
        serializer.is_valid(raise_exception=True)

        user = USER.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
            user_type=user_type
        )
        user.verification_code = generate_random_digits(6)
        user.save()
        send_verification_email(user.email, user.verification_code)

        return Response({'detail': f'{user.full_name} is created successfully'}, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['GET'],
        url_name='user_me',
        permission_classes=[IsAuthenticated, ],
        url_path='me',
        serializer_class=UserDetailSerializer,
    )
    def user_me(self, request, *args, **kwargs):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['POST'],
        url_name='verify',
        permission_classes=[IsAuthenticated, ],
        url_path='verification',
        serializer_class=UserVerificationSerializer
    )
    def user_verification(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if data.get('verification_code') == str(user.verification_code):
            user.is_verified = True
            user.save()
            return Response({'message': 'Successfully Verified'}, status=status.HTTP_200_OK)

        return Response({'message': 'Sorry the Pin Code doesnot match'}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['POST'],
        url_name='forgot_password',
        permission_classes=[AllowAny, ],
        url_path='forgot-password',
        serializer_class=UserDetailSerializer
    )
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['email']
        ),
        responses={
            200: 'Password reset email sent',
            # Add more response codes and descriptions as needed
        }
    )
    def forgot_password(self, request, *args, **kwargs):
        data = request.data
        email = USER.objects.get(email=data.get('email'))
        email.verification_code = generate_random_digits(6)
        email.save()
        send_forgor_password_email(email.email, email.verification_code)
        return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
