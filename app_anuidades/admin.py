from django.contrib import admin
from .models import AnuidadeModel

@admin.register(AnuidadeModel)
class AnuidadeModelAdmin(admin.ModelAdmin):
    list_display = ('ano', 'valor_anuidade', 'data_criacao')
    search_fields = ('ano',)
    list_filter = ('ano',)
