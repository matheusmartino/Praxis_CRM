# apps/core/management/commands/seed_crm.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


from apps.accounts.models import Perfil
from apps.core.enums import PerfilUsuario

User = get_user_model()


class Command(BaseCommand):
    help = "Seed inicial do CRM: cria vendedor e gestor"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🌱 Iniciando seed do CRM..."))

        self.criar_usuario(
            username="vendedor",
            email="vendedor@crm.local",
            senha="123456",
            papel=PerfilUsuario.VENDEDOR,
            nome="Vendedor Padrão",
        )

        self.criar_usuario(
            username="gestor",
            email="gestor@crm.local",
            senha="123456",
            papel=PerfilUsuario.GESTOR,
            nome="Gestor Padrão",
        )

        self.stdout.write(self.style.SUCCESS("✅ Seed finalizado com sucesso"))

    def criar_usuario(self, username, email, senha, papel, nome):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": nome,
                "is_active": True,
            },
        )

        if created:
            user.set_password(senha)
            user.save()

            Perfil.objects.create(
                user=user,
                papel=papel,
            )

            self.stdout.write(
                self.style.SUCCESS(f"✔ Usuário {username} ({papel}) criado")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"⚠ Usuário {username} já existe, ignorado")
            )
