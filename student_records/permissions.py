from rest_framework.permissions import BasePermission

def _in_group(user, *names):
    return (
        user and user.is_authenticated
        and user.groups.filter(name__in=names).exists()
    )

class IsAdminUser(BasePermission):
    """Allow only members of the 'Admin' group."""
    message = 'Access denied: Admin role required.'
    def has_permission(self, request, view):
        return _in_group(request.user, 'Admin')

class IsAdminOrFaculty(BasePermission):
    """Allow Admin and Faculty groups."""
    message = 'Access denied: Admin or Faculty role required.'
    def has_permission(self, request, view):
        return _in_group(request.user, 'Admin', 'Faculty')

class IsAdminFacultyOrOwner(BasePermission):
    """View-level: authenticated. Object-level: Admin/Faculty always;
    Student only if they own the record."""
    message = 'Access denied: you can only view your own record.'
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if _in_group(request.user, 'Admin', 'Faculty'):
            return True
        return obj.owner == request.user