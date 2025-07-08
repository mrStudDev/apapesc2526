from django.urls import path
from . import views

app_name = 'app_defeso'

urlpatterns = [
    
    path('defeso/lancamento/', views.DefesosLancamentoView.as_view(), name='lancamento_defeso'),
    path('controle/<int:pk>/edit/', views.ControleBeneficioEditView.as_view(), name='controle_beneficio_edit'),
    path('processamento/proximo/', views.proximo_controle_para_processar, name='proximo_controle_para_processar'),
    path('processamento/resetar-rodada/', views.resetar_rodada_processamento, name='resetar_rodada_processamento'),
]
