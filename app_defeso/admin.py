# app_defeso/admin.py

from django.contrib import admin
from .models import (
    LeiFederalPrevidenciaria,
    DecretosModel,
    PortariasModel,
    InstrucoesNormativasModel,
    Especie,
    PeriodoDefesoOficial,
    SeguroDefesoBeneficioModel,
    ControleBeneficioModel,
    ProcessamentoSeguroDefesoModel
)
from simple_history.admin import SimpleHistoryAdmin

@admin.register(LeiFederalPrevidenciaria)
class LeiFederalPrevidenciariaAdmin(admin.ModelAdmin):
    search_fields = ['numero']
    list_display = ['numero', 'data_publicacao']
    list_filter = ['data_publicacao']

@admin.register(DecretosModel)
class DecretosModelAdmin(admin.ModelAdmin):
    search_fields = ['numero']
    list_display = ['numero', 'data_publicacao']
    list_filter = ['data_publicacao']

@admin.register(PortariasModel)
class PortariasModelAdmin(admin.ModelAdmin):
    search_fields = ['numero', 'orgao_emissor']
    list_display = ['numero', 'ano', 'orgao_emissor', 'tipo', 'estado']
    list_filter = ['tipo', 'estado', 'orgao_emissor', 'ano']

@admin.register(InstrucoesNormativasModel)
class InstrucoesNormativasModelAdmin(admin.ModelAdmin):
    search_fields = ['numero', 'orgao_emissor']
    list_display = ['numero', 'orgao_emissor', 'data_publicacao']
    list_filter = ['orgao_emissor', 'data_publicacao']

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    search_fields = ['nome_popular', 'nome_cientifico']
    list_display = ['nome_popular', 'nome_cientifico']

@admin.register(PeriodoDefesoOficial)
class PeriodoDefesoOficialAdmin(admin.ModelAdmin):
    search_fields = ['especie__nome_popular', 'orgao_definidor']
    list_display = ['especie', 'orgao_definidor', 'data_inicio_oficial', 'data_fim_oficial', 'estado']
    list_filter = ['orgao_definidor', 'estado', 'data_inicio_oficial']

@admin.register(SeguroDefesoBeneficioModel)
class SeguroDefesoBeneficioModelAdmin(admin.ModelAdmin):
    search_fields = ['especie_alvo__nome_popular']
    list_display = ['especie_alvo', 'estado', 'ano_concessao', 'data_inicio', 'data_fim']
    list_filter = ['estado', 'ano_concessao', 'data_inicio']

@admin.register(ControleBeneficioModel)
class ControleBeneficioModelAdmin(SimpleHistoryAdmin):
    search_fields = ['associado__user__username', 'beneficio__especie_alvo__nome_popular']
    list_display = ['associado', 'beneficio', 'status_pedido', 'data_solicitacao', 'data_concessao']
    list_filter = ['status_pedido', 'data_solicitacao', 'data_concessao', 'beneficio']
    readonly_fields = ['criado_em', 'atualizado_em']
    

@admin.register(ProcessamentoSeguroDefesoModel)
class ProcessamentoSeguroDefesoAdmin(admin.ModelAdmin):
    list_display = (
        'beneficio',
        'rodada',
        'usuario',
        'status',
        'iniciado_em',
        'concluido_em',
        'indice_atual',
        'total_associados',
        'processada',
    )
    list_filter = ('beneficio', 'rodada', 'status', 'usuario')
    search_fields = ('beneficio__especie_alvo__nome', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    readonly_fields = ('iniciado_em', 'concluido_em', 'atualizado_em')
    ordering = ('-iniciado_em',)

    fieldsets = (
        (None, {
            'fields': (
                'beneficio',
                'rodada',
                'usuario',
                'status',
                'indice_atual',
                'total_associados',
                'processada',
                'observacoes',
            )
        }),
        ('Datas', {
            'fields': ('iniciado_em', 'concluido_em', 'atualizado_em')
        }),
    )    

