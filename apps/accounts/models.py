from django.conf import settings
from django.db import models

from apps.core.enums import PerfilUsuario


class Perfil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    papel = models.CharField(
        max_length=10,
        choices=PerfilUsuario.choices,
        default=PerfilUsuario.VENDEDOR,
        verbose_name="Papel",
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.get_papel_display()}"

    @property
    def is_admin(self):
        return self.papel == PerfilUsuario.ADMIN

    @property
    def is_vendedor(self):
        return self.papel == PerfilUsuario.VENDEDOR

    @property
    def is_gestor(self):
        return self.papel == PerfilUsuario.GESTOR
