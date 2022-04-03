from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.customer:
            return True
        else:
            return request.user.phone.endswith('88')