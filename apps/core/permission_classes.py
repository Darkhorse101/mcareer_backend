from django.conf import settings
from rest_framework.permissions import BasePermission, SAFE_METHODS 

from apps.users.models import Organization, OrganizationStaff


class PermissionMixin(BasePermission):
    @staticmethod
    def get_related_organization(request):
        try:
            return OrganizationStaff.objects.filter(
                is_archived=False,
                organization__slug=request.headers.get('org'),
                staff=request.user
            ).first()
        except OrganizationStaff.DoesNotExist:
            return

    @staticmethod
    def is_authenticated(request):
        return bool(
            request.user and
            request.user.is_authenticated
        )

    @staticmethod
    def is_anonymous(request):
        return bool(
            request.user and
            request.user.is_anonymous
        )
    
    @staticmethod
    def is_owner(request):
        org_slug = request.headers.get('org')
        assert bool(org_slug), 'Organization not provided'
        assert Organization.objects.get(
            slug=org_slug), "Organization Doesn't Exist"
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.owned_organizations.get(
                **{'slug':org_slug})
        )
    
    def is_organization_admin(self, request, view):
        org_slug = request.headers.get('org')
        assert bool(org_slug), 'Organization not provided'
        assert Organization.objects.get(
            slug=org_slug).exists(), "Organization Doesn't Exist"

        is_admin = bool(
            request.user and
            request.user.is_authenticated and
            self.get_related_organization(request)
        )

        is_owner = Organization.objects.get(
            slug=org_slug).owner == request.user

        if is_owner:           
            return True
        
        if is_admin:
            return True        

        if not hasattr(view, 'admin_permission') or not isinstance(
            view.admin_permission, dict
        ):
            raise NotImplementedError(
                "key-value pair for organization's admin permission must be provided"
            )
        
        # allow admins to perform all actions, useful in running tests
        if not (
            hasattr(settings, 'ALLOW_ALL_PERMISSIONS') and
            settings.ALLOW_ALL_PERMISSIONS
        ):

            if 'all' in view.admin_permission:
                # Skip permission check and allow access
                return True

            action = 'update' if view.action == 'partial_update' else view.action
            permission = view.admin_permission.get(action, [])

            if permission == ['all']:
                return True

            return set(permission).intersection(
                set(self.get_related_organization(request).permissions)
            )
        else:
            return is_admin


class SuperuserPermission(PermissionMixin):
    """
    Grant all permissions to the superusers
    """
    def has_permission(self, request, view):
        return self.is_superuser(request)

class OwnerPermission(PermissionMixin):
    "Permission class to handle the organization owners"
    def has_permission(self, request, view):
        return self.is_owner(request)

class AnonymousPermission(PermissionMixin):
    """Permission class to handle anonymous requests"""

    def has_permission(self, request, view):
        return self.is_anonymous(request)


class OrganizationAdminPermission(PermissionMixin):
    """
    Permission class to handle permission for organization
    level admins
    """

    def has_permission(self, request, view):
        return self.is_organization_admin(self, request, view)


class AnonymousOrAdminPermission(PermissionMixin):
    """
    Permission class to handle requests for anonymous or admin 
    permissions
    """
    def has_permission(self, request, view):
        return bool(
            self.is_anonymous(request) or
            self.is_admin(request, view)
        )


class IsOwnerOrAdminReadOnly(PermissionMixin):
    """
    Permission class that makes sure unsafe actions are performed
    by the organization owner only whereas safe methods can be performed
    by the organization admin
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return self.is_organization_admin(request, view)

        return self.is_owner(request) 