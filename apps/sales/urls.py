from django.urls import path

from apps.sales.views import (
    FollowUpEditView,
    InteracaoCreateView,
    InteracaoListView,
    MetasPorVendedorView,
    MinhaMetaView,
    MinhasPendenciasView,
    OportunidadeAvancarView,
    OportunidadeCreateView,
    OportunidadeDetailView,
    OportunidadeListView,
    OportunidadePerdidaView,
    OportunidadesSemFollowUpView,
)

app_name = "sales"

urlpatterns = [
    path("oportunidades/", OportunidadeListView.as_view(), name="oportunidade_list"),
    path("oportunidades/nova/", OportunidadeCreateView.as_view(), name="oportunidade_create"),
    path("oportunidades/<int:pk>/", OportunidadeDetailView.as_view(), name="oportunidade_detail"),
    path("oportunidades/<int:pk>/avancar/", OportunidadeAvancarView.as_view(), name="oportunidade_avancar"),
    path("oportunidades/<int:pk>/perdida/", OportunidadePerdidaView.as_view(), name="oportunidade_perdida"),
    path("oportunidades/<int:pk>/followup/", FollowUpEditView.as_view(), name="followup_edit"),
    path("interacoes/", InteracaoListView.as_view(), name="interacao_list"),
    path("interacoes/nova/", InteracaoCreateView.as_view(), name="interacao_create"),
    # Metas comerciais
    path("minha-meta/", MinhaMetaView.as_view(), name="minha_meta"),
    path("metas/", MetasPorVendedorView.as_view(), name="metas_por_vendedor"),
    # Follow-up
    path("pendencias/", MinhasPendenciasView.as_view(), name="minhas_pendencias"),
    path("sem-followup/", OportunidadesSemFollowUpView.as_view(), name="sem_followup"),
]
