from rest_framework.permissions import BasePermission


class IsMethodDelete(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'DELETE'


class IsMethodPost(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'


class IsMethodGet(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'


class IsMethodPatch(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'PATCH'
