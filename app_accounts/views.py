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
        'associado':'dashboard_associado',
    }

    template = user_type_template_map.get(user.user_type, 'dashboard_cliente.html')
    return render(request, f'dashboards/{template}')

class AcessoNegadoView(TemplateView):
    template_name = 'accounts/acesso_negado.html'


User = get_user_model()
@login_required
@user_passes_test(lambda u: u.is_superuser or u.user_type == 'admin_associacao')
def criar_usuario_fake(request):
    prefix = "0000FAKE"
    base_username = "0000fake"
    base_email = "@email.com"
    password = "@senhafake"
    user_type_default = "cliente"

    # Busca maior número usado
    existing_fakes = User.objects.filter(username__startswith=base_username)
    next_number = 1

    if existing_fakes.exists():
        ultimos_numeros = [
            int(u.username.replace(base_username, '').replace('User_fake', '')) 
            for u in existing_fakes if u.username.replace(base_username, '').replace('User_fake', '').isdigit()
        ]
        next_number = max(ultimos_numeros) + 1 if ultimos_numeros else 1

    # Formata número
    numero_formatado = f"{next_number:04d}"

    # Cria campos
    username = f"{base_username}{numero_formatado}"
    email = f"{prefix}{numero_formatado}{base_email}"

    # Cria usuário
    novo_user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        user_type=user_type_default
    )

    messages.success(request, f"✅ Usuário fake criado: {username} / {email}")

    # Redireciona para lista ou edição
    return redirect('app_associacao:list_users')  