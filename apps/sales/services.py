from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone

from apps.core.enums import EtapaOportunidade
from apps.sales.models import Interacao, MetaComercial, Oportunidade

ORDEM_ETAPAS = [
    EtapaOportunidade.PROSPECCAO,
    EtapaOportunidade.QUALIFICACAO,
    EtapaOportunidade.PROPOSTA,
    EtapaOportunidade.NEGOCIACAO,
    EtapaOportunidade.FECHAMENTO,
]


def criar_oportunidade(*, titulo, cliente, vendedor, valor_estimado=0, descricao=""):
    return Oportunidade.objects.create(
        titulo=titulo,
        cliente=cliente,
        vendedor=vendedor,
        valor_estimado=valor_estimado,
        descricao=descricao,
        etapa=EtapaOportunidade.PROSPECCAO,
    )


def avancar_etapa(*, oportunidade):
    """Avança a oportunidade para a próxima etapa do pipeline."""
    if oportunidade.etapa == EtapaOportunidade.PERDIDA:
        raise ValidationError("Oportunidade perdida não pode avançar.")

    if oportunidade.etapa == EtapaOportunidade.FECHAMENTO:
        raise ValidationError("Oportunidade já está na etapa final.")

    idx_atual = ORDEM_ETAPAS.index(oportunidade.etapa)
    oportunidade.etapa = ORDEM_ETAPAS[idx_atual + 1]
    oportunidade.save(update_fields=["etapa", "atualizado_em"])
    return oportunidade


def marcar_perdida(*, oportunidade):
    """Marca uma oportunidade como perdida."""
    if oportunidade.etapa == EtapaOportunidade.FECHAMENTO:
        raise ValidationError("Oportunidade fechada não pode ser marcada como perdida.")
    oportunidade.etapa = EtapaOportunidade.PERDIDA
    oportunidade.save(update_fields=["etapa", "atualizado_em"])
    return oportunidade


def registrar_interacao(*, oportunidade, tipo, descricao, user):
    return Interacao.objects.create(
        oportunidade=oportunidade,
        tipo=tipo,
        descricao=descricao,
        criado_por=user,
    )


# =============================================================================
# METAS COMERCIAIS
# =============================================================================


def calcular_realizado(*, vendedor, mes, ano):
    """
    Calcula o valor realizado (vendas fechadas) de um vendedor no mês/ano.
    Realizado = soma de valor_estimado das oportunidades com etapa FECHAMENTO.
    """
    total = Oportunidade.objects.filter(
        vendedor=vendedor,
        etapa=EtapaOportunidade.FECHAMENTO,
        atualizado_em__month=mes,
        atualizado_em__year=ano,
    ).aggregate(total=Sum("valor_estimado"))["total"]

    return total or Decimal("0.00")


def calcular_pipeline(*, vendedor, mes, ano):
    """
    Calcula o valor em pipeline (oportunidades abertas) de um vendedor no mês/ano.
    Pipeline = soma de valor_estimado das oportunidades que NÃO são FECHAMENTO nem PERDIDA.
    """
    total = Oportunidade.objects.filter(
        vendedor=vendedor,
        criado_em__month=mes,
        criado_em__year=ano,
    ).exclude(
        etapa__in=[EtapaOportunidade.FECHAMENTO, EtapaOportunidade.PERDIDA]
    ).aggregate(total=Sum("valor_estimado"))["total"]

    return total or Decimal("0.00")


def calcular_status_meta(*, valor_meta, pipeline):
    """
    Calcula o status da meta baseado no pipeline.
    - OK: pipeline >= 1.5 × valor_meta
    - ATENCAO: pipeline >= valor_meta
    - RISCO: pipeline < valor_meta
    """
    if valor_meta <= 0:
        return "OK"

    if pipeline >= valor_meta * Decimal("1.5"):
        return "OK"
    elif pipeline >= valor_meta:
        return "ATENCAO"
    else:
        return "RISCO"


def obter_meta_vendedor(*, vendedor, mes=None, ano=None):
    """
    Obtém a meta do vendedor para o mês/ano especificado.
    Se não informado, usa o mês/ano atual.
    Retorna dict com meta, realizado, pipeline, percentual e status.
    """
    if mes is None or ano is None:
        hoje = timezone.now()
        mes = mes or hoje.month
        ano = ano or hoje.year

    try:
        meta = MetaComercial.objects.get(vendedor=vendedor, mes=mes, ano=ano)
        valor_meta = meta.valor_meta
    except MetaComercial.DoesNotExist:
        meta = None
        valor_meta = Decimal("0.00")

    realizado = calcular_realizado(vendedor=vendedor, mes=mes, ano=ano)
    pipeline = calcular_pipeline(vendedor=vendedor, mes=mes, ano=ano)

    if valor_meta > 0:
        percentual = round((realizado / valor_meta) * 100, 1)
    else:
        percentual = Decimal("0.0")

    status = calcular_status_meta(valor_meta=valor_meta, pipeline=pipeline)

    return {
        "meta": meta,
        "valor_meta": valor_meta,
        "realizado": realizado,
        "pipeline": pipeline,
        "percentual": percentual,
        "status": status,
        "mes": mes,
        "ano": ano,
    }


def listar_metas_vendedores(*, mes=None, ano=None):
    """
    Lista todas as metas do mês/ano com os cálculos de cada vendedor.
    Usado pela visão do gestor.
    """
    if mes is None or ano is None:
        hoje = timezone.now()
        mes = mes or hoje.month
        ano = ano or hoje.year

    metas = MetaComercial.objects.filter(mes=mes, ano=ano).select_related("vendedor")
    resultado = []

    for meta in metas:
        dados = obter_meta_vendedor(vendedor=meta.vendedor, mes=mes, ano=ano)
        resultado.append(dados)

    return resultado, mes, ano
