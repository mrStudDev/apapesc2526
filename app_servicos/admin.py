from django.contrib import admin
from .models import ServicoModel, EntradaFinanceiraModel, PagamentoEntrada


class PagamentoEntradaInline(admin.TabularInline):
    model = PagamentoEntrada
    extra = 1
    readonly_fields = ("valor_pago", "data_pagamento", "registrado_por")

@admin.register(ServicoModel)
class ServicoModelAdmin(admin.ModelAdmin):
    list_display = ("id", "associado", "natureza_servico", "tipo_servico", "status_servico", "valor", "data_inicio", "ultima_alteracao", "criado_por")
    list_filter = ("natureza_servico", "tipo_servico", "status_servico", "data_inicio", "associacao")
    search_fields = ("associado__user__first_name", "associado__user__last_name", "associado__id")
    inlines = [PagamentoEntradaInline]
    autocomplete_fields = ["associado", "associacao", "reparticao", "criado_por"]
    date_hierarchy = "data_inicio"
    ordering = ("-data_inicio",)

@admin.register(EntradaFinanceiraModel)
class EntradaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ("id", "servico", "valor", "valor_pagamento", "status_pagamento", "forma_pagamento", "parcelamento", "data_entrada", "pago")
    list_filter = ("status_pagamento", "forma_pagamento", "parcelamento", "data_entrada")
    search_fields = ("servico__associado__user__first_name", "servico__associado__user__last_name", "servico__id")
    autocomplete_fields = ["servico"]
    date_hierarchy = "data_entrada"
    ordering = ("-data_entrada",)

