from django import forms
from .models import ServicoModel, EntradaFinanceiraModel, PagamentoEntrada
from django.forms import DateInput


class ServicoForm(forms.ModelForm):
    class Meta:
        model = ServicoModel
        fields = [
            'natureza_servico', 'tipo_servico', 'associacao', 'reparticao',
            'valor', 'status_servico', 'content', 'associado'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 50, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['associacao'].required = True
        self.fields['reparticao'].required = True

        self.fields['natureza_servico'].widget.attrs.update({'class': 'js-natureza-servico'})
        self.fields['tipo_servico'].widget.attrs.update({'class': 'js-tipo-servico'})
        self.fields['tipo_servico'].widget.attrs.update({'class': 'js-tipo-servico'})
        self.fields['status_servico'].widget.attrs.update({'class': 'js-status-servico'})

                    
        

        
class EntradaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = EntradaFinanceiraModel
        fields = [
            'servico',
            'forma_pagamento',
            'parcelamento',
            'valor',
            'pago',
            'valor_pagamento',
        ]
        widgets = {
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'parcelamento': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['forma_pagamento'].required = True
        self.fields['parcelamento'].required = True
        self.fields['valor'].required = True

class PagamentoEntradaForm(forms.ModelForm):
    class Meta:
        model = PagamentoEntrada
        fields = [
            'servico',
            'valor_pago',
            'data_pagamento',
            'registrado_por',
        ]
        widgets = {
            'data_pagamento': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        