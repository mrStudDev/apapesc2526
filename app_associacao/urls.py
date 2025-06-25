from django.urls import path
from . import views

# App Space Name
app_name = 'app_associacao'

urlpatterns = [
    # Creates
    path('novo-integrante/', views.IntegranteCreateView.as_view(), name='create_integrante'),
    path('nova-associacao/', views.AssociacaoCreateView.as_view(), name='create_associacao'),
    path('nova-reparticao/', views.ReparticaoCreateView.as_view(), name='create_reparticao'),
    path('nova-profissao/', views.ProfissaoCreateView.as_view(), name='create_profissao'),
    path('novo-municipio/', views.MunicipioCreateView.as_view(), name='create_municipio'),
    path('novo-cargo/', views.CargosCreateView.as_view(), name='create_cargo'),
    
    # Lists
    path('lista-associacoes/', views.AssociacaoListView.as_view(), name='list_associacoes'),
    path('lista-reparticoes/', views.ReparticoesListView.as_view(), name='list_reparticoes'),
    path('lista-integrantes/', views.IntegrantesListView.as_view(), name='list_integrantes'),
    path('lista-municipios/', views.MunicipiosListView.as_view(), name='list_municipios'),
    path('lista-profissoes/', views.ProfissoesListView.as_view(), name='list_profissoes'),
    path('lista-cargos/', views.CargosListView.as_view(), name='list_cargos'),
    
    # Lista e Edição de USUÁRIOS =========================================================
    path('lista-usuarios/', views.UserListView.as_view(), name='list_users'),
    path('editar-usuario/<int:pk>/', views.UserUpdateView.as_view(), name='edit_user'),
    #-------------------------------------------------------------------------
    
    # Edits
    path('editar-associacao/<int:pk>/', views.AssociacaoUpdateView.as_view(), name='edit_associacao'),
    path('editar-reparticao/<int:pk>/', views.ReparticaoUpdateView.as_view(), name='edit_reparticao'),
    path('editar-integrante/<int:pk>/', views.IntegranteUpdateView.as_view(), name='edit_integrante'),
    path('editar-municipio/<int:pk>/', views.MunicipioUpdateView.as_view(), name='edit_municipio'),
    path('editar-profissao/<int:pk>/', views.ProfissaoUpdateView.as_view(), name='edit_profissao'),
    path('editar-cargo/<int:pk>/', views.CargoUpdateView.as_view(), name='edit_cargo'),

    # Singles
    path('detalhes-associacao/<int:pk>/', views.AssociacaoDetailView.as_view(), name='single_associacao'),
    path('detalhes-reparticao/<int:pk>/', views.ReparticaoDetailView.as_view(), name='single_reparticao'),
    path('detalhes-integrante/<int:pk>/', views.IntegranteDetailView.as_view(), name='single_integrante'),
    
    # AJAX
    path('ajax/reparticoes-por-associacao/', views.reparticoes_por_associacao, name='ajax_reparticoes_por_associacao'),
    path('ajax/municipios-por-reparticao/', views.municipios_por_reparticao, name='municipios_por_reparticao'),
 

]