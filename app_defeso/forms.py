# app_defeso/forms.py
from django import forms
from .models import ControleBeneficioModel
from django.forms import DateInput

class ControleBeneficioForm(forms.ModelForm):
    class Meta:
        model = ControleBeneficioModel
        fields = [
            'numero_protocolo',
            'status_pedido',
            'data_solicitacao',
            'data_concessao',
            'motivo_exigencia',
            'motivo_negativa',
            'anotacoes',
            'resultado_final',
            'comprovante_protocolo',
        ]
        widgets = {
            'data_solicitacao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_concessao': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'motivo_exigencia': forms.Textarea(attrs={'rows': 4}),
            'motivo_negativa': forms.Textarea(attrs={'rows': 4}),
            'anotacoes': forms.Textarea(attrs={'rows': 4}),
            'resultado_final': forms.Textarea(attrs={'rows': 4}),
        }
