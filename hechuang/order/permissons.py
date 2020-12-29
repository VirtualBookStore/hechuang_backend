from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
from rest_framework.request import Request


class IsOwner(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        return obj.user == request.user


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated and not IsAdminUser