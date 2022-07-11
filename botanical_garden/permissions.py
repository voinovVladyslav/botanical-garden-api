from rest_framework import permissions
from django.contrib.auth.models import Group


class IsManagerOrReadOnly(permissions.BasePermission):
    message = 'Only manager has access to news management'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_groups = request.user.groups.filter(name='manager').first()
        manager = Group.objects.filter(name='manager').first()
        
        return manager == user_groups
