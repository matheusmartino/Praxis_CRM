from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils import timezone
from django.views.generic import TemplateView

from apps.core.enums import EtapaOportunidade, StatusCliente
from apps.core.mixins import GestorRequiredMixin
from apps.crm.models import Cliente
from apps.sales.models import Oportunidade

User = get_user_model()

# Número de dias para considerar uma oportunidade como "parada"
DIAS_OPORTUNIDADE_PARADA = 7


class DashboardGestorView(GestorRequiredMixin, TemplateView):
    """Dashboard principal do gestor comercial."""

    template_name = "gestao/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total de leads (clientes PROVISORIOS)
        context["total_leads"] = Cliente.objects.filter(
            status=StatusCliente.PROVISORIO
        ).count()

        # Total de clientes ativos
        context["total_clientes_ativos"] = Cliente.objects.filter(
            status=StatusCliente.ATIVO
        ).count()

        # Total de oportunidades (excluindo PERDIDA e FECHAMENTO)
        oportunidades_abertas = Oportunidade.objects.exclude(
            etapa__in=[EtapaOportunidade.PERDIDA, EtapaOportunidade.FECHAMENTO]
        )
        context["total_oportunidades"] = oportunidades_abertas.count()

        # Valor total em pipeline
        context["valor_pipeline"] = (
            oportunidades_abertas.aggregate(total=Sum("valor_estimado"))["total"] or 0
        )

        # Oportunidades fechadas (ganhas)
        context["total_fechadas"] = Oportunidade.objects.filter(
            etapa=EtapaOportunidade.FECHAMENTO
        ).count()

        # Valor total fechado
        context["valor_fechado"] = (
            Oportunidade.objects.filter(etapa=EtapaOportunidade.FECHAMENTO).aggregate(
                total=Sum("valor_estimado")
            )["total"]
            or 0
        )

        # Alerta visual: oportunidades sem follow-up ou paradas
        data_limite = timezone.now() - timedelta(days=DIAS_OPORTUNIDADE_PARADA)

        # Oportunidades sem data_follow_up
        sem_followup = oportunidades_abertas.filter(data_follow_up__isnull=True).count()

        # Oportunidades paradas há mais de X dias
        paradas = oportunidades_abertas.filter(atualizado_em__lt=data_limite).count()

        context["oportunidades_sem_followup"] = sem_followup
        context["oportunidades_paradas"] = paradas
        context["dias_oportunidade_parada"] = DIAS_OPORTUNIDADE_PARADA
        context["total_alerta_disciplina"] = sem_followup + paradas

        return context


class LeadsPorVendedorView(GestorRequiredMixin, TemplateView):
    """Relatório de leads por vendedor."""

    template_name = "gestao/leads_por_vendedor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Dados agregados por vendedor
        vendedores_data = []

        vendedores = User.objects.filter(
            clientes_criados__isnull=False
        ).distinct()

        for vendedor in vendedores:
            # Leads criados (clientes PROVISORIOS)
            leads_criados = Cliente.objects.filter(
                criado_por=vendedor, status=StatusCliente.PROVISORIO
            ).count()

            # Total de clientes criados pelo vendedor
            total_clientes = Cliente.objects.filter(criado_por=vendedor).count()

            # Oportunidades criadas pelo vendedor
            oportunidades_criadas = Oportunidade.objects.filter(
                vendedor=vendedor
            ).count()

            # Oportunidades criadas a partir de leads desse vendedor
            clientes_ids = Cliente.objects.filter(criado_por=vendedor).values_list(
                "id", flat=True
            )
            oportunidades_leads = Oportunidade.objects.filter(
                cliente_id__in=clientes_ids
            ).count()

            # Percentual de conversao
            if total_clientes > 0:
                conversao = round((oportunidades_leads / total_clientes) * 100, 1)
            else:
                conversao = 0

            vendedores_data.append(
                {
                    "vendedor": vendedor,
                    "leads_criados": leads_criados,
                    "total_clientes": total_clientes,
                    "oportunidades_criadas": oportunidades_criadas,
                    "oportunidades_leads": oportunidades_leads,
                    "conversao": conversao,
                }
            )

        # Ordenar por leads criados (decrescente)
        vendedores_data.sort(key=lambda x: x["leads_criados"], reverse=True)
        context["vendedores"] = vendedores_data

        return context


class PipelineGeralView(GestorRequiredMixin, TemplateView):
    """Visao geral do pipeline de vendas."""

    template_name = "gestao/pipeline_geral.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pipeline por etapa
        etapas_data = []
        for etapa_code, etapa_label in EtapaOportunidade.choices:
            oportunidades = Oportunidade.objects.filter(etapa=etapa_code)
            quantidade = oportunidades.count()
            valor_total = oportunidades.aggregate(total=Sum("valor_estimado"))[
                "total"
            ] or 0

            etapas_data.append(
                {
                    "etapa": etapa_label,
                    "etapa_code": etapa_code,
                    "quantidade": quantidade,
                    "valor_total": valor_total,
                }
            )

        context["etapas"] = etapas_data

        # Pipeline por vendedor
        vendedores_pipeline = []
        vendedores = User.objects.filter(oportunidades__isnull=False).distinct()

        for vendedor in vendedores:
            oportunidades_abertas = Oportunidade.objects.filter(
                vendedor=vendedor
            ).exclude(etapa__in=[EtapaOportunidade.PERDIDA, EtapaOportunidade.FECHAMENTO])

            quantidade = oportunidades_abertas.count()
            valor_total = oportunidades_abertas.aggregate(total=Sum("valor_estimado"))[
                "total"
            ] or 0

            # Detalhamento por etapa
            etapas_vendedor = []
            for etapa_code, etapa_label in EtapaOportunidade.choices:
                if etapa_code in [EtapaOportunidade.PERDIDA, EtapaOportunidade.FECHAMENTO]:
                    continue
                ops_etapa = oportunidades_abertas.filter(etapa=etapa_code)
                qtd = ops_etapa.count()
                if qtd > 0:
                    etapas_vendedor.append(
                        {
                            "etapa": etapa_label,
                            "quantidade": qtd,
                            "valor": ops_etapa.aggregate(total=Sum("valor_estimado"))[
                                "total"
                            ]
                            or 0,
                        }
                    )

            vendedores_pipeline.append(
                {
                    "vendedor": vendedor,
                    "quantidade": quantidade,
                    "valor_total": valor_total,
                    "etapas": etapas_vendedor,
                }
            )

        # Ordenar por valor total (decrescente)
        vendedores_pipeline.sort(key=lambda x: x["valor_total"], reverse=True)
        context["vendedores_pipeline"] = vendedores_pipeline

        return context
