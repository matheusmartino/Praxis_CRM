from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from apps.core.enums import PerfilUsuario


class VendedorRequiredMixin(LoginRequiredMixin):
    """Permite acesso a usuários com perfil VENDEDOR, GESTOR ou ADMIN."""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if hasattr(request.user, "perfil"):
            if request.user.perfil.papel in (
                PerfilUsuario.VENDEDOR,
                PerfilUsuario.GESTOR,
                PerfilUsuario.ADMIN,
            ):
                return response
        raise PermissionDenied


class AdminRequiredMixin(LoginRequiredMixin):
    """Permite acesso apenas a usuários com perfil ADMIN."""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if hasattr(request.user, "perfil"):
            if request.user.perfil.papel == PerfilUsuario.ADMIN:
                return response
        raise PermissionDenied


class GestorRequiredMixin(LoginRequiredMixin):
    """Permite acesso apenas a usuários com perfil GESTOR ou ADMIN."""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if hasattr(request.user, "perfil"):
            if request.user.perfil.papel in (
                PerfilUsuario.GESTOR,
                PerfilUsuario.ADMIN,
            ):
                return response
        raise PermissionDenied


class VendedorWriteMixin(LoginRequiredMixin):
    """
    Permite escrita apenas a VENDEDOR ou ADMIN.
    GESTOR é redirecionado com mensagem informativa (não recebe 403).

    Atributo opcional:
        redirect_url_name: nome da URL para redirecionamento (default: 'home')
    """

    redirect_url_name = "home"

    def dispatch(self, request, *args, **kwargs):
        # Primeiro verifica autenticação
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Verifica se tem perfil e qual o papel
        if hasattr(request.user, "perfil"):
            papel = request.user.perfil.papel

            # VENDEDOR e ADMIN podem criar
            if papel in (PerfilUsuario.VENDEDOR, PerfilUsuario.ADMIN):
                return super().dispatch(request, *args, **kwargs)

            # GESTOR é redirecionado com mensagem amigável
            if papel == PerfilUsuario.GESTOR:
                messages.warning(
                    request,
                    "Apenas vendedores podem criar registros. "
                    "Seu perfil de gestor permite apenas visualização.",
                )
                return redirect(self.redirect_url_name)

        # Outros casos: sem perfil ou perfil desconhecido
        raise PermissionDenied
