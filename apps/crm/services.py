from django.core.exceptions import PermissionDenied, ValidationError

from apps.core.enums import PerfilUsuario, StatusCliente
from apps.crm.models import Cliente


def criar_cliente(
    *,
    nome,
    telefone="",
    email="",
    tipo,
    user,
    cnpj_cpf="",
    nome_contato_principal="",
    telefone_contato="",
    email_contato="",
):
    """Cria um cliente. Vendedores sempre criam com status PROVISORIO."""
    status = StatusCliente.PROVISORIO
    if hasattr(user, "perfil") and user.perfil.papel == PerfilUsuario.ADMIN:
        status = StatusCliente.ATIVO

    cliente = Cliente(
        nome=nome,
        telefone=telefone,
        email=email,
        tipo=tipo,
        status=status,
        criado_por=user,
        cnpj_cpf=cnpj_cpf,
        nome_contato_principal=nome_contato_principal,
        telefone_contato=telefone_contato,
        email_contato=email_contato,
    )

    try:
        cliente.clean()
    except ValidationError:
        # Model rejeita ATIVO sem cnpj_cpf — rebaixa para PROVISORIO
        cliente.status = StatusCliente.PROVISORIO

    cliente.save()
    return cliente


def ativar_cliente(*, cliente, user):
    """Ativa um cliente. Apenas admins podem ativar. Exige CNPJ/CPF preenchido."""
    if not hasattr(user, "perfil") or user.perfil.papel != PerfilUsuario.ADMIN:
        raise PermissionDenied("Apenas administradores podem ativar clientes.")
    if not cliente.cnpj_cpf:
        raise ValidationError("CNPJ/CPF é obrigatório para ativar um cliente.")
    cliente.status = StatusCliente.ATIVO
    cliente.save(update_fields=["status", "atualizado_em"])
    return cliente


def inativar_cliente(*, cliente, user):
    """Inativa um cliente. Apenas admins podem inativar."""
    if not hasattr(user, "perfil") or user.perfil.papel != PerfilUsuario.ADMIN:
        raise PermissionDenied("Apenas administradores podem inativar clientes.")
    cliente.status = StatusCliente.INATIVO
    cliente.save(update_fields=["status", "atualizado_em"])
    return cliente
