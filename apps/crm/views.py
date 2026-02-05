from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from apps.core.mixins import VendedorRequiredMixin, VendedorWriteMixin
from apps.crm.forms import ClienteForm
from apps.crm.models import Cliente
from apps.crm.services import criar_cliente


class ClienteListView(VendedorRequiredMixin, ListView):
    model = Cliente
    template_name = "crm/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request.user, "perfil") and self.request.user.perfil.is_vendedor:
            qs = qs.filter(criado_por=self.request.user)
        return qs


class ClienteCreateView(VendedorWriteMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "crm/cliente_form.html"
    success_url = reverse_lazy("crm:cliente_list")
    redirect_url_name = "crm:cliente_list"  # Redirecionamento para GESTOR

    def form_valid(self, form):
        criar_cliente(
            nome=form.cleaned_data["nome"],
            telefone=form.cleaned_data["telefone"],
            email=form.cleaned_data["email"],
            tipo=form.cleaned_data["tipo"],
            user=self.request.user,
            cnpj_cpf=form.cleaned_data["cnpj_cpf"],
            nome_contato_principal=form.cleaned_data["nome_contato_principal"],
            telefone_contato=form.cleaned_data["telefone_contato"],
            email_contato=form.cleaned_data["email_contato"],
        )
        return redirect(self.success_url)


class ClienteDetailView(VendedorRequiredMixin, DetailView):
    model = Cliente
    template_name = "crm/cliente_detail.html"
    context_object_name = "cliente"

    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request.user, "perfil") and self.request.user.perfil.is_vendedor:
            qs = qs.filter(criado_por=self.request.user)
        return qs
