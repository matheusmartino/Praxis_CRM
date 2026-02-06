from django import forms

from apps.sales.models import Interacao, Oportunidade


class OportunidadeForm(forms.ModelForm):
    class Meta:
        model = Oportunidade
        fields = ["titulo", "cliente", "valor_estimado", "descricao"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "valor_estimado": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class InteracaoForm(forms.ModelForm):
    class Meta:
        model = Interacao
        fields = ["oportunidade", "tipo", "descricao"]
        widgets = {
            "oportunidade": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class FollowUpForm(forms.ModelForm):
    """Formulário para editar campos de follow-up."""

    class Meta:
        model = Oportunidade
        fields = ["proxima_acao", "data_follow_up"]
        widgets = {
            "proxima_acao": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Ligar para confirmar proposta",
            }),
            "data_follow_up": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        }
