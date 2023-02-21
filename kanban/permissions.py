from rest_framework import permissions


class IsKanbanMembersList(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False

class IsKanbanMembersItem(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False