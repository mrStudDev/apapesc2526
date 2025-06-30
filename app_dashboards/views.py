from core.views.base_imports import *
from core.views.app_dashboards_imports import *

# Create your views here.

class SuperDashboardView(View):
    template_name = 'dashboards/dashboard_superuser.html'

    def get(self, request, *args, **kwargs):
        # ANUIDADES
        # Todos os lançamentos de anuidades
        anuidades = AnuidadeModel.objects.all().order_by('-ano')

        # 1. Quantidade de anos lançados
        qtd_anos_lancados = anuidades.count()

        # 2. Dados por ano
        dados_por_ano = []
        total_anuidades_aplicadas = 0
        total_valor_aplicado = 0

        for anuidade in anuidades:
            qtd_aplicadas = anuidade.anuidades_associados.count()
            valor_total_ano = qtd_aplicadas * anuidade.valor_anuidade

            total_anuidades_aplicadas += qtd_aplicadas
            total_valor_aplicado += valor_total_ano

            dados_por_ano.append({
                'ano': anuidade.ano,
                'qtd_aplicadas': qtd_aplicadas,
                'valor_total_ano': valor_total_ano,
                'valor_unitario': anuidade.valor_anuidade,
            })
        
        # ASSOCIADOS
        associados = AssociadoModel.objects.all()
        total_cadastrados = associados.count()
        associados_ativos = associados.filter(status='associado_lista_ativo').count()
        associados_aposentados = associados.filter(status='associado_lista_aposentado').count()
        total_pagantes = associados_ativos + associados_aposentados
        

        context = {
            # Anuidades
            'qtd_anos_lancados': qtd_anos_lancados,
            'dados_por_ano': dados_por_ano,
            'total_anuidades_aplicadas': total_anuidades_aplicadas,
            'total_valor_aplicado': total_valor_aplicado,
            # Associados
            'total_cadastrados': total_cadastrados,
            'associados_ativos': associados_ativos,
            'associados_aposentados': associados_aposentados,
            'total_pagantes': total_pagantes,
            
        }
        return render(request, self.template_name, context)