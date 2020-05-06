from rest_framework import permissions

class MyUserPermissions(permissions.BasePermission):
## Пользовательское разрешение для разграничения прав доступа
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return (request.user == obj.avtor or request.user.username=="Administrator")

class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return (request.user.id == obj.author.id or request.user.username == "Administrator")
9