from apps.core.enums import PerfilUsuario


class GestorReadOnlyAdminMixin:
    """
    Mixin para tornar ModelAdmin read-only para usuarios GESTOR.
    ADMIN mantem acesso total.
    """

    def _is_gestor(self, request):
        if hasattr(request.user, "perfil"):
            return request.user.perfil.papel == PerfilUsuario.GESTOR
        return False

    def has_add_permission(self, request):
        if self._is_gestor(request):
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if self._is_gestor(request):
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if self._is_gestor(request):
            return False
        return super().has_delete_permission(request, obj)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if self._is_gestor(request):
            # Remove todas as actions para GESTOR
            return {}
        return actions
