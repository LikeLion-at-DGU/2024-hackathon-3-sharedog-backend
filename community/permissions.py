from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import UserProfile

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        return obj.writer == user_profile or request.user.is_superuser