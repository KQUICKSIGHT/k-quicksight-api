from rest_framework.permissions import BasePermission
from user.models import User
from user_role.models import UserRole


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        return request.user.is_authenticated and UserRole.objects.filter(user=request.user, role__name='admin').exists()


class IsSubscriberUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'subscriber' role
        return request.user.is_authenticated and UserRole.objects.filter(user=request.user, role__name='subscriber').exists()

class IsAdminOrSubscriber(BasePermission):
    def has_permission(self, request,view):
        return request.user.is_authenticated and (UserRole.objects.filter(user=request.user, role__name='subscriber').exists() or UserRole.objects.filter(user=request.user, role__name='admin').exists())
