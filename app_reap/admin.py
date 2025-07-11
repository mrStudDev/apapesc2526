# app_defeso/admin.py
from django.contrib import admin
from .models import REAPdoAno, ProcessamentoREAPModel

@admin.register(REAPdoAno)
class REAPdoAnoAdmin(admin.ModelAdmin):
    list_display = ('associado', 'ano', 'status_resposta', 'rodada', 'processada', 'em_processamento_por', 'atualizado_em')
    search_fields = ('associado__user__username',)
    list_filter = ('ano', 'status_resposta', 'rodada', 'processada')

@admin.register(ProcessamentoREAPModel)
class ProcessamentoREAPAdmin(admin.ModelAdmin):
    list_display = ('ano', 'rodada', 'usuario', 'status', 'iniciado_em', 'concluido_em')
    list_filter = ('ano', 'rodada', 'status')
