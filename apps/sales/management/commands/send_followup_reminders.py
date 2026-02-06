"""
Management command para enviar lembretes de follow-up por e-mail.

Uso:
    python manage.py send_followup_reminders

Este comando deve ser executado diariamente (via cron ou task scheduler).
Envia no máximo 1 e-mail por vendedor por dia.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.enums import EtapaOportunidade, PerfilUsuario
from apps.sales.models import Oportunidade

User = get_user_model()


class Command(BaseCommand):
    help = "Envia lembretes de follow-up por e-mail para vendedores"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simula o envio sem enviar e-mails reais",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        hoje = timezone.now().date()

        self.stdout.write(f"Verificando follow-ups para {hoje}...")

        # Buscar vendedores com oportunidades com follow-up para hoje
        vendedores_com_followup = self._get_vendedores_com_followup_hoje(hoje)

        if not vendedores_com_followup:
            self.stdout.write(self.style.SUCCESS("Nenhum follow-up agendado para hoje."))
            return

        enviados = 0
        erros = 0

        for vendedor, quantidade in vendedores_com_followup:
            if dry_run:
                self.stdout.write(
                    f"[DRY-RUN] Enviaria e-mail para {vendedor.email} "
                    f"({quantidade} oportunidade(s))"
                )
                enviados += 1
            else:
                sucesso = self._enviar_email_lembrete(vendedor, quantidade)
                if sucesso:
                    enviados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"E-mail enviado para {vendedor.email}")
                    )
                else:
                    erros += 1
                    self.stdout.write(
                        self.style.ERROR(f"Erro ao enviar para {vendedor.email}")
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Concluído: {enviados} e-mail(s) enviado(s), {erros} erro(s)."
            )
        )

    def _get_vendedores_com_followup_hoje(self, hoje):
        """
        Retorna lista de tuplas (vendedor, quantidade) para vendedores
        que possuem oportunidades com follow-up para hoje.
        """
        # Oportunidades abertas com follow-up para hoje
        oportunidades_hoje = Oportunidade.objects.filter(
            data_follow_up=hoje
        ).exclude(
            etapa__in=[EtapaOportunidade.FECHAMENTO, EtapaOportunidade.PERDIDA]
        ).select_related("vendedor")

        # Agrupar por vendedor
        vendedores_dict = {}
        for op in oportunidades_hoje:
            vendedor = op.vendedor
            # Verificar se o vendedor tem e-mail válido
            if not vendedor.email:
                continue
            # Verificar se é um vendedor (não enviar para gestor/admin)
            if hasattr(vendedor, "perfil") and vendedor.perfil.papel != PerfilUsuario.VENDEDOR:
                continue

            if vendedor not in vendedores_dict:
                vendedores_dict[vendedor] = 0
            vendedores_dict[vendedor] += 1

        return list(vendedores_dict.items())

    def _enviar_email_lembrete(self, vendedor, quantidade):
        """Envia e-mail de lembrete para o vendedor."""
        try:
            assunto = "Praxis CRM - Lembrete de Follow-up"

            if quantidade == 1:
                mensagem = (
                    f"Olá {vendedor.first_name or vendedor.username},\n\n"
                    f"Você possui 1 oportunidade com follow-up agendado para hoje.\n\n"
                    f"Acesse o Praxis CRM para visualizar.\n\n"
                    f"Atenciosamente,\n"
                    f"Equipe Praxis CRM"
                )
            else:
                mensagem = (
                    f"Olá {vendedor.first_name or vendedor.username},\n\n"
                    f"Você possui {quantidade} oportunidades com follow-up agendado para hoje.\n\n"
                    f"Acesse o Praxis CRM para visualizar.\n\n"
                    f"Atenciosamente,\n"
                    f"Equipe Praxis CRM"
                )

            send_mail(
                subject=assunto,
                message=mensagem,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[vendedor.email],
                fail_silently=False,
            )
            return True

        except Exception as e:
            self.stderr.write(f"Erro ao enviar e-mail: {e}")
            return False
