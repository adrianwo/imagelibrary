from rest_framework import permissions


class CanGenerateLinksPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.generate_link
