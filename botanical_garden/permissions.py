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


class IsAuthorOrIsManagerOrReadOnly(permissions.BasePermission):
    message = 'Only manager can view all messages'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user_groups = request.user.groups.filter(name='manager').first()
        manager = Group.objects.filter(name='manager').first()
        is_manager = manager == user_groups

        return request.user == obj.user or is_manager 


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = "You can't modify this, you're not the author"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user

class ReadOnly(permissions.BasePermission):
    message = "Read only"

    def has_permission(self, request, view):
        if request.method == "POST":
            return False
        return True 

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class NoDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return False
        return True 

class NoCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return True
