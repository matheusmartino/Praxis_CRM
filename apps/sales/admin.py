from django.contrib import admin

from apps.core.admin_mixins import GestorReadOnlyAdminMixin
from apps.sales.models import Interacao, MetaComercial, Oportunidade


class InteracaoInline(admin.TabularInline):
    model = Interacao
    extra = 0
    readonly_fields = ("criado_por", "criado_em")


@admin.register(Oportunidade)
class OportunidadeAdmin(GestorReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("titulo", "cliente", "vendedor", "etapa", "valor_estimado", "criado_em")
    list_filter = ("etapa", "criado_em")
    search_fields = ("titulo", "cliente__nome")
    readonly_fields = ("criado_em", "atualizado_em")
    inlines = [InteracaoInline]


@admin.register(Interacao)
class InteracaoAdmin(GestorReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("oportunidade", "tipo", "criado_por", "criado_em")
    list_filter = ("tipo", "criado_em")
    search_fields = ("descricao", "oportunidade__titulo")
    readonly_fields = ("criado_por", "criado_em")


@admin.register(MetaComercial)
class MetaComercialAdmin(GestorReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("vendedor", "mes", "ano", "valor_meta", "criado_por", "criado_em")
    list_filter = ("ano", "mes")
    search_fields = ("vendedor__username", "vendedor__first_name", "vendedor__last_name")
    readonly_fields = ("criado_por", "criado_em")
    autocomplete_fields = ["vendedor"]

    def save_model(self, request, obj, form, change):
        if not change:  # Apenas na criação
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
