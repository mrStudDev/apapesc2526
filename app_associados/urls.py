from django.urls import path
from . import views

# App Space Name
app_name = 'app_associados'

urlpatterns = [
    # Creates
    path('novo-associado/', views.AssociadoCreateView.as_view(), name='create_associado'),
    path('editar-associado/<int:pk>/', views.AssociadoUpdateView.as_view(), name='edit_associado'),
    
    # Edits
    
    # Lists
    path('associados/', views.AssociadoListView.as_view(), name='list_associados'),
    
    # Singles
    path('associado/<int:pk>/', views.AssociadoSingleView.as_view(), name='single_associado'),
    
    # AJAX
    #path('ajax/reparticoes-por-associacao/', views.reparticoes_por_associacao, name='ajax_reparticoes_por_associacao'),
    #path('ajax/municipios-por-reparticao/', views.municipios_por_reparticao, name='municipios_por_reparticao'),

]