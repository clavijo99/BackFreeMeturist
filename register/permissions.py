from rest_framework import permissions


class CommentsOwnerUser(permissions.BasePermission):
    """ permission validated if comment register belong to user authenticated """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
