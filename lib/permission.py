from rest_framework import permissions


class ChernobylPermission(permissions.BasePermission):

    def _global_permission(self, request, view):
        if not request.user.is_authenticated:
            return view.action in ["list", "retrieve"]
        # staff and admin user can do anythings (like delete object )
        elif request.user.is_staff or request.user.is_superuser:
            return True
        # lambda user can creat, upate ( partial update ) and get
        return view.action not in ["update", "destroy"]

    def has_permission(self, request, view):
        return self._global_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnlyLamda(permissions.BasePermission):

    def _global_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # staff and admin user can do anythings (like delete object )
        elif request.user.is_staff or request.user.is_superuser:
            return True
        # lambda user can read
        return view.action in ["list", "retrieve"]

    def has_permission(self, request, view):
        return self._global_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
