from django.contrib import admin
from .models import INSSGuiaDoMes, ProcessamentoINSSModel

@admin.register(INSSGuiaDoMes)
class INSSGuiaDoMesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'associado', 'ano', 'mes', 'rodada', 'status_emissao',
        'status_acesso', 'processada', 'em_processamento_por', 'atualizado_em'
    )
    list_filter = ('ano', 'mes', 'rodada', 'processada', 'status_emissao', 'status_acesso')
    search_fields = ('associado__nome', 'associado__cpf')
    readonly_fields = ('criado_em', 'atualizado_em')
    ordering = ('-ano', '-mes', 'rodada', 'associado')

@admin.register(ProcessamentoINSSModel)
class ProcessamentoINSSModelAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'ano', 'mes', 'rodada', 'usuario', 'status',
        'iniciado_em', 'concluido_em'
    )
    list_filter = ('ano', 'mes', 'rodada', 'status', 'usuario')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('iniciado_em', 'atualizado_em', 'concluido_em')
    ordering = ('-iniciado_em',)
