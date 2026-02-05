from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from apps.accounts.models import Perfil
from apps.core.admin_mixins import GestorReadOnlyAdminMixin


class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = "Perfil"
    extra = 0  # Não cria formulários extras

    def has_add_permission(self, request, obj=None):
        # Nunca permite adicionar Perfil via inline (signal é responsável)
        return False


class UserAdmin(GestorReadOnlyAdminMixin, BaseUserAdmin):
    inlines = (PerfilInline,)

    def get_inlines(self, request, obj):
        # Mostra inline apenas na EDIÇÃO (obj existe), não na CRIAÇÃO
        if obj is None:
            return []
        return self.inlines


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
