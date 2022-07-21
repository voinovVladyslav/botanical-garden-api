from rest_framework import permissions
from django.contrib.auth.models import Group


class IsManager(permissions.BasePermission):
    message = "You're not the manager"

    def has_permission(self, request, view):
        group = Group.objects.get(name='manager')
        return group in request.user.groups.all()
