from django.urls import path

from . import views

app_name = "gestao"

urlpatterns = [
    path("", views.DashboardGestorView.as_view(), name="dashboard"),
    path(
        "leads-por-vendedor/",
        views.LeadsPorVendedorView.as_view(),
        name="leads_por_vendedor",
    ),
    path("pipeline/", views.PipelineGeralView.as_view(), name="pipeline_geral"),
]
