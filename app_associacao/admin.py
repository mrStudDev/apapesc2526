from django.contrib import admin
from .models import (
    IntegrantesModel,
    CargosModel,
    MunicipiosModel,
    ProfissoesModel,
    AssociacaoModel,
    ReparticoesModel,
)

@admin.register(IntegrantesModel)
class IntegrantesAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'celular', 'email', 'cargo', 'associacao', 'reparticao')
    search_fields = ('user__username', 'cpf', 'email')
    list_filter = ('estado_civil', 'cargo', 'associacao', 'reparticao')

@admin.register(CargosModel)
class CargosAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(MunicipiosModel)
class MunicipiosAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'uf')
    search_fields = ('municipio',)
    list_filter = ('uf',)

@admin.register(ProfissoesModel)
class ProfissoesAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(AssociacaoModel)
class AssociacaoAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'razao_social', 'cnpj', 'administrador', 'presidente')
    search_fields = ('nome_fantasia', 'razao_social', 'cnpj')
    list_filter = ('uf',)

@admin.register(ReparticoesModel)
class ReparticoesAdmin(admin.ModelAdmin):
    list_display = ('nome_reparticao', 'associacao', 'delegado', 'municipio')
    search_fields = ('nome_reparticao',)
    list_filter = ('uf', 'associacao')
