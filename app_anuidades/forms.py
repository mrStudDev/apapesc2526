from django import forms
import datetime
from .models import Pagamento, AnuidadeModel, DescontoAnuidade

class AnuidadeForm(forms.ModelForm):
    class Meta:
        model = AnuidadeModel
        fields = ['ano', 'valor_anuidade']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ano'].initial = datetime.date.today().year  # valor default

    def clean_ano(self):
        ano = int(self.cleaned_data['ano'])
        if AnuidadeModel.objects.filter(ano=ano).exists():
            raise forms.ValidationError(f"Já existe anuidade cadastrada para o ano {ano}.")
        return ano
    
            
# Formulário simples para Pagamento
class PagamentoForm(forms.Form):
    valor = forms.DecimalField(max_digits=10, decimal_places=2, label='Valor Pago')
    comprovante_up = forms.FileField(required=False, label='Comprovante do Pagamento')
    
# Formulário simples para Desconto
class DescontoAnuidadeForm(forms.ModelForm):
    class Meta:
        model = DescontoAnuidade
        fields = ['valor_desconto', 'motivo']
        # OU: exclude = []   (se quiser todos os campos, mas normalmente fields é melhor)        