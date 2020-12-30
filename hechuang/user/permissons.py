from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser, SAFE_METHODS, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.request import Request


class IsOwner(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        return bool(request.user) and request.user.is_authenticated and obj.user == request.user


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user) and request.user.is_authenticated and not request.user.is_staff


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        print(view.action)
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user) and request.user.is_authenticated and request.user.is_staff

