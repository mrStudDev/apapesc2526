from django.urls import path
from . import views

# App Space Name
app_name = 'app_servicos'

urlpatterns = [

    path('servico/create/<int:associado_id>/', views.ServicoCreateView.as_view(), name='create_servico'),
    path('servico/detalhes/<int:pk>/', views.ServicoSingleView.as_view(), name='single_servico'),
    path('entrada/create/<int:servico_id>/', views.EntradaCreateView.as_view(), name='create_entrada'),

   
]
