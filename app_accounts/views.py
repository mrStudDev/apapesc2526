from core.views.base_imports import *
from core.views.app_accounts_imports import *

@login_required
def dashboard(request):
    user = request.user

    if user.is_superuser:
        return render(request, 'dashboards/dashboard_superuser.html')
    
    user_type_template_map = {
        'admin_associacao': 'dashboard_admin.html',
        'diretor': 'dashboard_diretor.html',
        'presidente': 'dashboard_presidente.html',
        'delagado': 'dashboard_deleagdo.html',
        'financeiro': 'dashboard_financeiro.html',
        'recursos_humanos': 'dashboard_recursos_humanos.html',
        'auxiliar_associacao': 'dashboard_aux_associacao.html',
        'auxiliar_reparticao': 'dashboard_aux_reparticao.html',
        'auxiliar_extra': 'dashboard_aux_extra.html',
        'cliente_vip': 'dashboard_cliente_vip.html',
        'cliente': 'dashboard_cliente.html',
    }

    template = user_type_template_map.get(user.user_type, 'dashboard_cliente.html')
    return render(request, f'dashboards/{template}')

class AcessoNegadoView(TemplateView):
    template_name = 'accounts/acesso_negado.html'


