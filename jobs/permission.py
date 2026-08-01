from rest_framework import permissions
from .models import Company,Job,Application
class IsJobCompanyOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.company.recruiter== request.user
    