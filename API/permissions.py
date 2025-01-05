from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permission permettant uniquement aux admins d'accéder à une ressource.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'admin')  # Vérifie si l'utilisateur est un admin.


class IsEnqueteur(BasePermission):
    """
    Permission permettant uniquement aux enquêteurs d'accéder à une ressource.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'enqueteur')  # Vérifie si l'utilisateur est un enquêteur.


class IsPublishedOrAdmin(BasePermission):
    """
    Permission permettant aux enquêteurs d'accéder uniquement aux enquêtes publiées,
    et aux admins d'accéder à tout.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'admin'):
            return True  # Les admins ont un accès complet.
        if hasattr(request.user, 'enqueteur') and obj.published:
            return True  # Les enquêteurs peuvent accéder aux enquêtes publiées.
        return False
