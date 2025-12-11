from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin users can do anything.
    Non-admin users can only read (GET).
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admin users
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners or admin to edit.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin can do anything
        if request.user and request.user.is_staff:
            return True
        
        # Check if user is the owner
        if hasattr(obj, 'customer'):
            return obj.customer.email == request.user.email
        
        return False