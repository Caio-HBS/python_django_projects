from rest_framework import permissions


class IsStaffOrOwnerPermission(permissions.BasePermission):
    """
        Allows for only owner or staff to view list/make changes to posts.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
