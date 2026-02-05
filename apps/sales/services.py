from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import F, Sum
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


# =============================================================================
# FOLLOW-UP E DISCIPLINA COMERCIAL
# =============================================================================


def calcular_status_follow_up(data_follow_up):
    """
    Calcula o status do follow-up baseado na data.
    - EM_DIA: data_follow_up > hoje
    - HOJE: data_follow_up == hoje
    - ATRASADO: data_follow_up < hoje
    - SEM_DATA: data_follow_up é None
    """
    if data_follow_up is None:
        return "SEM_DATA"

    hoje = timezone.now().date()

    if data_follow_up > hoje:
        return "EM_DIA"
    elif data_follow_up == hoje:
        return "HOJE"
    else:
        return "ATRASADO"


def calcular_dias_atraso(data_follow_up):
    """Calcula quantos dias de atraso (negativo se no futuro)."""
    if data_follow_up is None:
        return None

    hoje = timezone.now().date()
    diferenca = (hoje - data_follow_up).days
    return diferenca


def listar_pendencias_vendedor(*, vendedor):
    """
    Lista oportunidades do vendedor com follow-up atrasado ou para hoje.
    Retorna lista ordenada por mais atrasadas primeiro.
    """
    hoje = timezone.now().date()

    oportunidades = Oportunidade.objects.filter(
        vendedor=vendedor,
        data_follow_up__lte=hoje,
    ).exclude(
        etapa__in=[EtapaOportunidade.FECHAMENTO, EtapaOportunidade.PERDIDA]
    ).select_related("cliente").order_by("data_follow_up")

    resultado = []
    for oportunidade in oportunidades:
        dias_atraso = calcular_dias_atraso(oportunidade.data_follow_up)
        status = calcular_status_follow_up(oportunidade.data_follow_up)
        resultado.append({
            "oportunidade": oportunidade,
            "dias_atraso": dias_atraso,
            "status": status,
        })

    return resultado


def listar_oportunidades_sem_follow_up(*, dias_parada=7):
    """
    Lista oportunidades sem follow-up OU paradas há mais de X dias.
    Usado pela visão do gestor.
    """
    hoje = timezone.now()
    data_limite = hoje - timedelta(days=dias_parada)

    # Oportunidades abertas (excluindo fechadas e perdidas)
    oportunidades_abertas = Oportunidade.objects.exclude(
        etapa__in=[EtapaOportunidade.FECHAMENTO, EtapaOportunidade.PERDIDA]
    ).select_related("cliente", "vendedor")

    # Filtrar: sem data_follow_up OU sem movimentação há X dias
    oportunidades = oportunidades_abertas.filter(
        data_follow_up__isnull=True
    ) | oportunidades_abertas.filter(
        atualizado_em__lt=data_limite
    )

    # Remover duplicatas e ordenar
    oportunidades = oportunidades.distinct().order_by("atualizado_em")

    resultado = []
    for oportunidade in oportunidades:
        dias_sem_movimentacao = (hoje.date() - oportunidade.atualizado_em.date()).days
        tem_follow_up = oportunidade.data_follow_up is not None
        resultado.append({
            "oportunidade": oportunidade,
            "dias_sem_movimentacao": dias_sem_movimentacao,
            "tem_follow_up": tem_follow_up,
        })

    return resultado


def atualizar_follow_up(*, oportunidade, proxima_acao, data_follow_up):
    """Atualiza os campos de follow-up de uma oportunidade."""
    oportunidade.proxima_acao = proxima_acao or ""
    oportunidade.data_follow_up = data_follow_up
    oportunidade.save(update_fields=["proxima_acao", "data_follow_up", "atualizado_em"])
    return oportunidade


# =============================================================================
# LEMBRETES E ALERTAS
# =============================================================================


def contar_followups_hoje(*, vendedor):
    """
    Conta quantas oportunidades do vendedor têm follow-up para hoje.
    Usado para lembrete visual no dashboard.
    """
    hoje = timezone.now().date()
    return Oportunidade.objects.filter(
        vendedor=vendedor,
        data_follow_up=hoje,
    ).exclude(
        etapa__in=[EtapaOportunidade.FECHAMENTO, EtapaOportunidade.PERDIDA]
    ).count()


def contar_oportunidades_alerta(*, dias_parada=7):
    """
    Conta oportunidades sem follow-up ou paradas há mais de X dias.
    Usado para alerta visual no dashboard do gestor.
    Retorna dict com contagens separadas.
    """
    hoje = timezone.now()
    data_limite = hoje - timedelta(days=dias_parada)

    oportunidades_abertas = Oportunidade.objects.exclude(
        etapa__in=[EtapaOportunidade.FECHAMENTO, EtapaOportunidade.PERDIDA]
    )

    sem_followup = oportunidades_abertas.filter(data_follow_up__isnull=True).count()
    paradas = oportunidades_abertas.filter(atualizado_em__lt=data_limite).count()

    return {
        "sem_followup": sem_followup,
        "paradas": paradas,
        "total": sem_followup + paradas,
    }
