from django.contrib import admin
from .models import UploadsDocs, TipoDocumentoUp

@admin.register(UploadsDocs)
class UploadsDocsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'enviado_por', 'data_envio']
    list_filter = ['data_envio', 'tipo']

@admin.register(TipoDocumentoUp)
class TipoDocumentoUpAdmin(admin.ModelAdmin):
    search_fields = ['nome']
