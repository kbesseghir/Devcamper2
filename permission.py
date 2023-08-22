from rest_framework import permissions

class IsPublisherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role == 'publisher' or user.is_staff)



class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.request.method == 'POST':
              return IsPublisherOrAdmin().has_permission(request, view)
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and (user == obj.user or user.is_staff)
    

class IsOwner(permissions.BasePermission):
    
    

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_authenticated and (user == obj.user )

class IsUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow access to authenticated users with role "user" or "admin"
        return (
            request.user.is_authenticated
            and (request.user.role == 'user' or request.user.is_staff)
        )