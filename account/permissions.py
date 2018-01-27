from django.contrib.auth.models import Group
from rest_framework import permissions


class IsStoreManager(permissions.IsAuthenticated):
    """
        check user role is staff or vendor
    """

    def has_permission(self, request, view):
        name = "Store manager"
        group, created = Group.objects.get_or_create(name=name)
        if group in request.user.groups.all():
            return True
