from django.contrib import admin
from django.urls import include, path

from apps.accounts.views import home_view, landing_view, manual_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("crm/", include("apps.crm.urls")),
    path("sales/", include("apps.sales.urls")),
    path("gestao/", include("apps.gestao.urls")),
    path("manual/", manual_view, name="manual"),
    path("dashboard/", home_view, name="home"),  # Dashboard do usuário logado
    path("", landing_view, name="landing"),  # Landing page como raiz
]
