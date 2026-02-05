from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import render

from apps.accounts.forms import LoginForm
from apps.crm.models import Cliente
from apps.sales.models import Oportunidade


class LoginView(auth_views.LoginView):
    template_name = "registration/login.html"
    authentication_form = LoginForm


class LogoutView(auth_views.LogoutView):
    next_page = "/accounts/login/"


@login_required
def home_view(request):
    user = request.user
    clientes_recentes = Cliente.objects.filter(criado_por=user).order_by("-criado_em")[:5]
    oportunidades_abertas = Oportunidade.objects.filter(vendedor=user).exclude(
        etapa__in=["FECHAMENTO", "PERDIDA"]
    )
    context = {
        "clientes_recentes": clientes_recentes,
        "oportunidades_abertas": oportunidades_abertas,
        "total_oportunidades": oportunidades_abertas.count(),
    }
    return render(request, "home.html", context)


@login_required
def manual_view(request):
    """Exibe o manual do usuário."""
    manual_path = settings.BASE_DIR / "docs" / "manual_usuario.html"
    if not manual_path.exists():
        raise Http404("Manual não encontrado.")
    return FileResponse(open(manual_path, "rb"), content_type="text/html")
