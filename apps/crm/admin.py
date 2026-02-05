from django.contrib import admin

from apps.core.admin_mixins import GestorReadOnlyAdminMixin
from apps.crm.models import Cliente
from apps.crm.services import ativar_cliente, inativar_cliente


@admin.action(description="Ativar clientes selecionados")
def ativar_clientes(modeladmin, request, queryset):
    for cliente in queryset:
        ativar_cliente(cliente=cliente, user=request.user)


@admin.action(description="Inativar clientes selecionados")
def inativar_clientes(modeladmin, request, queryset):
    for cliente in queryset:
        inativar_cliente(cliente=cliente, user=request.user)


@admin.register(Cliente)
class ClienteAdmin(GestorReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "nome", "cnpj_cpf", "tipo", "status",
        "nome_contato_principal", "telefone", "criado_por", "criado_em",
    )
    list_filter = ("tipo", "status", "criado_em")
    search_fields = ("nome", "cnpj_cpf", "nome_contato_principal")
    readonly_fields = ("criado_por", "criado_em", "atualizado_em")
    fieldsets = (
        (None, {
            "fields": ("nome", "cnpj_cpf", "tipo", "status"),
        }),
        ("Contato da empresa", {
            "fields": ("telefone", "email"),
        }),
        ("Contato principal", {
            "fields": ("nome_contato_principal", "telefone_contato", "email_contato"),
        }),
        ("Auditoria", {
            "fields": ("criado_por", "criado_em", "atualizado_em"),
        }),
    )
    actions = [ativar_clientes, inativar_clientes]
