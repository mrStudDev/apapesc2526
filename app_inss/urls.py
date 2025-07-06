from django.urls import path
from . import views

# App Space Name
app_name = 'app_inss'

urlpatterns = [

    path('lancamentos-inss/', views.LancamentosINSSListView.as_view(), name='lancamentos_inss'),
    path('processamento-inss/', views.ProcessamentoINSSDoMesView.as_view(), name='processamento_inss_do_mes'),
    path('resetar-processamento/', views.resetar_processamento, name='resetar_processamento'),

]
