from django.db import models


class TipoCliente(models.TextChoices):
    B2B = "B2B", "Pessoa Jurídica (B2B)"
    B2C = "B2C", "Pessoa Física (B2C)"


class StatusCliente(models.TextChoices):
    PROVISORIO = "PROVISORIO", "Provisório"
    ATIVO = "ATIVO", "Ativo"
    INATIVO = "INATIVO", "Inativo"


class TipoInteracao(models.TextChoices):
    LIGACAO = "LIGACAO", "Ligação"
    EMAIL = "EMAIL", "E-mail"
    REUNIAO = "REUNIAO", "Reunião"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    VISITA = "VISITA", "Visita"


class EtapaOportunidade(models.TextChoices):
    PROSPECCAO = "PROSPECCAO", "Prospecção"
    QUALIFICACAO = "QUALIFICACAO", "Qualificação"
    PROPOSTA = "PROPOSTA", "Proposta"
    NEGOCIACAO = "NEGOCIACAO", "Negociação"
    FECHAMENTO = "FECHAMENTO", "Fechamento"
    PERDIDA = "PERDIDA", "Perdida"


class PerfilUsuario(models.TextChoices):
    VENDEDOR = "VENDEDOR", "Vendedor"
    GESTOR = "GESTOR", "Gestor Comercial"
    ADMIN = "ADMIN", "Administrador"
