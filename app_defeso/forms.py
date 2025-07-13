# app_defeso/forms.py
from django import forms
from .models import (
    ControleBeneficioModel,
    SeguroDefesoBeneficioModel,
    DecretosModel,
    PeriodoDefesoOficial,
    PortariasModel,
    InstrucoesNormativasModel,
    LeiFederalPrevidenciaria,
    Especie
    )
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



class SeguroDefesoBeneficioForm(forms.ModelForm):
    class Meta:
        model = SeguroDefesoBeneficioModel
        fields = [
            'especie_alvo',
            'lei_federal',
            'decreto_regulamentador',
            'instrucao_normativa',
            'portaria_especifica',
            'estado',
            'ano_concessao',
            'data_inicio',
            'data_fim'
        ]
        widgets = {
            'especie_alvo': forms.Select(attrs={'class': 'form-control'}),
            'lei_federal': forms.Select(attrs={'class': 'form-control'}),
            'decreto_regulamentador': forms.Select(attrs={'class': 'form-control'}),
            'instrucao_normativa': forms.Select(attrs={'class': 'form-control'}),
            'portaria_especifica': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'ano_concessao': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000}),
            'data_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_fim': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        labels = {
            'especie_alvo': 'Espécie Alvo',
            'lei_federal': 'Lei Federal',
            'decreto_regulamentador': 'Decreto Regulamentador',
            'instrucao_normativa': 'Instrução Normativa',
            'portaria_especifica': 'Portaria Específica',
            'estado': 'Estado',
            'ano_concessao': 'Ano de Concessão',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Fim',
        }

class DecretosForm(forms.ModelForm):
    class Meta:
        model = DecretosModel
        fields = '__all__'
        widgets = {
            'data_publicacao': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class PeriodoDefesoOficialForm(forms.ModelForm):
    class Meta:
        model = PeriodoDefesoOficial
        fields = '__all__'
        widgets = {
            'data_inicio_oficial': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_fim_oficial': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),            
        }

class PortariasForm(forms.ModelForm):
    class Meta:
        model = PortariasModel
        fields = '__all__'
        widgets = {
            'data_publicacao': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            
        }

class InstrucoesNormativasForm(forms.ModelForm):
    class Meta:
        model = InstrucoesNormativasModel
        fields = '__all__'
        widgets = {
            'data_publicacao': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        
class EspeciesForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = '__all__'
       
class LeiFederalPrevidenciariaForm(forms.ModelForm):
    class Meta:
        model = LeiFederalPrevidenciaria
        fields = '__all__'
        widgets = {
            'data_publicacao': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
