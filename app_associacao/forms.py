from django import forms
from django.contrib.auth.models import Group
from app_accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.dateformat import DateFormat
from django.forms import DateInput

from core.validators import (
    validate_and_format_cpf,
    validate_and_format_celular,
    validate_and_format_cep,
    validate_and_format_cnpj,
)

from .models import (
    IntegrantesModel,
    AssociacaoModel,
    ReparticoesModel,
    MunicipiosModel,
    ProfissoesModel,
    CargosModel
)

# Fomrs Associação =======================================
class AssociacaoForm(forms.ModelForm):
    class Meta:
        model = AssociacaoModel
        fields = '__all__'
        widgets = {
            'data_abertura': forms.DateInput(attrs={'type': 'date'}),
            'data_encerramento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Explicitamente definindo o valor dos campos de data se a instância já estiver definida
        if self.instance and self.instance.pk:
            if self.instance.data_abertura:
                self.fields['data_abertura'].widget.attrs['value'] = self.instance.data_abertura.strftime('%Y-%m-%d')
            if self.instance.data_encerramento:
                self.fields['data_encerramento'].widget.attrs['value'] = self.instance.data_encerramento.strftime('%Y-%m-%d')
            
        # Verifica quais diretores estão vinculados a outra associação e desabilita-os
        diretores_ocupados = IntegrantesModel.objects.filter(
            diretores_associacao__isnull=False
        ).distinct()

        if self.instance.pk:
            diretores_ocupados = diretores_ocupados.exclude(
                diretores_associacao=self.instance
            )

        self.disabled_diretores = [diretor.id for diretor in diretores_ocupados]

        # IDs já selecionados (para marcar checked ao editar)
        self.selected_diretores = []
        if self.instance.pk:
            self.selected_diretores = list(self.instance.diretores.values_list('id', flat=True))

        # Recriar choices com labels informativos
        choices = []
        for diretor in self.fields['diretores'].queryset:
            label = f"{diretor.user.first_name} {diretor.user.last_name}"  # Ajuste conforme o seu modelo
            if diretor.id in self.disabled_diretores:
                label += " (Vinculado)"
            choices.append((diretor.id, label))

        self.fields['diretores'].choices = choices
        

    def clean_cnpj(self):
        return validate_and_format_cnpj(self.cleaned_data['cnpj'])

    def clean_cep(self):
        return validate_and_format_cep(self.cleaned_data.get('cep'))
# -----------------------------------------------------------------------

# Forms Repartições =======================================
class ReparticoesForm(forms.ModelForm):
    class Meta:
        model = ReparticoesModel
        fields = '__all__'
        widgets = {
            'data_abertura': forms.DateInput(attrs={'type': 'date'}),
            'data_encerramento': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Explicitamente definindo o valor dos campos de data se a instância já estiver definida
        if self.instance and self.instance.pk:
            if self.instance.data_abertura:
                self.fields['data_abertura'].widget.attrs['value'] = self.instance.data_abertura.strftime('%Y-%m-%d')
            if self.instance.data_encerramento:
                self.fields['data_encerramento'].widget.attrs['value'] = self.instance.data_encerramento.strftime('%Y-%m-%d')
            
        municipios_ocupados = MunicipiosModel.objects.filter(
            municipios_circunscricao__isnull=False
        ).distinct()

        if self.instance.pk:
            municipios_ocupados = municipios_ocupados.exclude(
                municipios_circunscricao=self.instance
            )

        self.disabled_municipios = [m.id for m in municipios_ocupados]

        # IDs já selecionados (para marcar checked ao editar)
        self.selected_municipios = []
        if self.instance.pk:
            self.selected_municipios = list(self.instance.municipios_circunscricao.values_list('id', flat=True))

        # Recriar choices com labels informativos
        choices = []
        for municipio in self.fields['municipios_circunscricao'].queryset:
            label = municipio.municipio
            if municipio.id in self.disabled_municipios:
                label += " (Vinculado)"
            choices.append((municipio.id, label))

        self.fields['municipios_circunscricao'].choices = choices
                
                
    def clean_celular(self):
        celular = self.cleaned_data.get('celular', '')
        return validate_and_format_celular(celular)

    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '')
        return validate_and_format_cep(cep)

# -----------------------------------------------------------------------
    
# Forms Integrantes =======================================
class IntegrantesForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Grupo"
    )

    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        required=True,
        label="Tipo de Usuário",
        initial='cliente'
    )    
    class Meta:
        model = IntegrantesModel
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
            'rg_data_emissao': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        user_initial = kwargs.pop('user_initial', None)
        associacao_id = kwargs.pop('associacao_id', None)
        super().__init__(*args, **kwargs)

        # Explicitamente definindo o valor dos campos de data se a instância já estiver definida
        if self.instance and self.instance.pk:
            if self.instance.rg_data_emissao:
                self.fields['rg_data_emissao'].widget.attrs['value'] = self.instance.data_nascimento.strftime('%Y-%m-%d')
                
            if self.instance.rg_data_emissao:
                self.fields['rg_data_emissao'].widget.attrs['value'] = self.instance.rg_data_emissao.strftime('%Y-%m-%d')
                
            if self.instance.data_entrada:
                self.fields['data_entrada'].widget.attrs['value'] = self.instance.data_entrada.strftime('%Y-%m-%d')
                
            if self.instance.data_saida:
                self.fields['data_saida'].widget.attrs['value'] = self.instance.data_saida.strftime('%Y-%m-%d')
                        
            
        # Atualiza o queryset de repartições com base na associação
        if self.instance and self.instance.associacao:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao=self.instance.associacao).distinct()

        # Atualiza os IDs dos campos para o JS funcionar
        self.fields['associacao'].widget.attrs.update({'id': 'id_associacao'})
        self.fields['reparticao'].widget.attrs.update({'id': 'id_reparticao'})

        # Se a instância já existe (edição), carrega o grupo associado ao usuário
        if self.instance and self.instance.pk:
            # Carrega o grupo do usuário associado (se existe)
            self.fields['group'].initial = self.instance.user.groups.first()  # Assumindo que é apenas 1 grupo por vez
            # Carregar o tipo de usuário (user_type) associado ao usuário
            self.fields['user_type'].initial = self.instance.user.user_type  # Aqui está a chave para carregar o tipo de usuário

        # Preenche o campo 'user' caso necessário
        if user_initial:
            self.fields['user'].initial = user_initial
            self.fields['user'].disabled = True

        # Durante a edição (se já existe um objeto), configura a repartição corretamente
        if self.instance.pk and self.instance.associacao:
            self.fields['reparticao'].queryset = ReparticoesModel.objects.filter(associacao=self.instance.associacao)
            # Preenche a repartição com a que já foi salva, se existir
            self.fields['reparticao'].initial = self.instance.reparticao
          

    def clean_cpf(self):
        return validate_and_format_cpf(self.cleaned_data['cpf'])

    def clean_celular(self):
        return validate_and_format_celular(self.cleaned_data['celular'])

    def clean_cep(self):
        return validate_and_format_cep(self.cleaned_data['cep'])
# -----------------------------------------------------------------

# Forms Cargos ======================
class CargosForm(forms.ModelForm):
    class Meta:
        model = CargosModel
        fields = '__all__'
        
# Forms Municípios ===================
class MunicipiosForm(forms.ModelForm):
    class Meta:
        model = MunicipiosModel
        fields = '__all__'
        
# Forms Pofissões ====================
class ProfissoesForm(forms.ModelForm):
    class Meta:
        model = ProfissoesModel
        fields = '__all__'
