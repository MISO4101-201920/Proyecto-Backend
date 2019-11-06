from rest_framework import permissions


class ProfesorOwnsInteractiveContent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        user_with_roll = user.get_real_instance()
        if user_with_roll.__class__.__name__ == 'Profesor' and obj is not None:
            return obj.contenido.profesor == user_with_roll
        else:
            return False
