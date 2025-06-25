from django.contrib import admin
from .models import AssociadoModel, PetrechoPesca

@admin.register(AssociadoModel)
class AssociadoAdmin(admin.ModelAdmin):
    list_display = ['user', 'cpf', 'celular', 'associacao', 'reparticao', 'data_filiacao']
    search_fields = ['cpf', 'user__username', 'user__email']
    list_filter = ['associacao', 'reparticao', 'status']
    ordering = ['user__username']

@admin.register(PetrechoPesca)
class PetrechoPescaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']
