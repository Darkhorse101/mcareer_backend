from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext as _
from django.contrib.auth.models import Permission, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField

from apps.core.serializers import DummySerializer, DynamicFieldsModelSerializer
from apps.core.validators import validate_attachment

USER = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['name', 'codename']


class UserPermissionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    permission_codenames = serializers.ListField(child=serializers.CharField())

    def validate_user_id(self, value):
        try:
            user = USER.objects.get(pk=value)
        except USER.DoesNotExist:
            raise serializers.ValidationError("Invalid user ID")
        return user


    def validate_permission_codenames(self, value):
        for codename in value:
            try:
                Permission.objects.get(codename=codename)
            except Permission.DoesNotExist:
                raise serializers.ValidationError(f"Invalid permission codename: {codename}")
        return value
    
class GroupSerializer(DynamicFieldsModelSerializer):
    permissions = PermissionSerializer(many=True, required=False)
    
    class Meta:
        model = Group
        fields = ('name', 'permissions')

    def create(self, validated_data):
        permissions_data = validated_data.pop('permissions', [])
        group = Group.objects.create(**validated_data)

        codenames = [item['codename'] for item in permissions_data]
        permissions = Permission.objects.filter(codename__in=codenames)
        group.permissions.set(permissions)

        return group

    def update(self, instance, validated_data):
        # Update the group instance with the validated data
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        permissions_data = validated_data.get('permissions', [])
        codenames = [item['codename'] for item in permissions_data]
        instance.permissions.set(Permission.objects.filter(codename__in=codenames))

        return instance
    

class PasswordChangeSerializer(DummySerializer):
    password1 = PasswordField(max_length=20, min_length=5)
    password2 = PasswordField(max_length=20, min_length=5)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 != password2:
            raise serializers.ValidationError(_(
                'Both Password must be same'
            ))
        return super().validate(attrs)


class UserDetailSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = USER
        read_only_fields = ('created_at', 'last_login', 'id')
        fields = (
            'id',
            'full_name',
            'email',
            'phone_number',
            'created_at',
            'is_staff',
            'last_login',
            'profile_picture',
            'is_verified',
        )
        extra_kwargs = {
            'full_name': {
                'required': True,
                'allow_blank': False
            },
            'profile_picture': {
                'required': False,
                'allow_null': True,
                'validators': [
                    FileExtensionValidator(
                        allowed_extensions=['jpg', 'png']
                    ),
                    validate_attachment
                ],
                'use_url': True
            },
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=USER.objects.all(),
                        lookup='iexact',
                        message=_("You cannot create account with this email address.")
                    )
                ]
            },
            'phone_number': {
                'validators': []
            }
        }

    def get_fields(self):
        fields = super().get_fields()
        if self.request and self.request.method.upper() == 'POST':
            fields['password1'] = PasswordField(max_length=20, min_length=5)
            fields['password2'] = PasswordField(max_length=20, min_length=5)
            fields['referral_code'] = serializers.CharField(
                max_length=10,
                allow_null=True,
                required=False,
                allow_blank=True
            )
        return fields

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(_(
                'Both Password must be same'
            ))

        phone_number = attrs.get('phone_number')

        user_qs = USER.objects.all()

        if self.instance:
            user_qs = user_qs.exclude(id=self.instance.id)

        if user_qs.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({
                'phone_number': _(
                    'You cannot create user with this phone number.'
                )
            })
        return super().validate(attrs)
    


class CustomTokenObtainPairSerializer(DummySerializer, TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserDetailSerializer(instance=self.user).data
        return data
    
    
class UserRegistrationSerializer(DummySerializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
    
        if len(password1) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.", 'password')

        return attrs
    
class UserVerificationSerializer(DummySerializer):
    verification_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        vaerification_code = attrs.get('verification_code')
        if len(vaerification_code) != 6:
            raise serializers.ValidationError("Your pin must be 6 Digits")
        return super().validate(attrs)