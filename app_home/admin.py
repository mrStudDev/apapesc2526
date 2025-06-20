from django.contrib import admin
from app_home.models import HomeModel

@admin.register(HomeModel)
class HomeModelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')  # Mostra esses campos na listagem
    search_fields = ('titulo',)             # Campo de busca no admin
