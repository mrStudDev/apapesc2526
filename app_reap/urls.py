from django.urls import path
from . import views

# App Space Name
app_name = 'app_reap'

urlpatterns = [
    path('lancamentos-reap/', views.LancamentosREAPListView.as_view(), name='lancamentos_reap'),
    path('processamento-reap/', views.ProcessamentoREAPdoAnoView.as_view(), name='processamento_reap_do_ano'),
    path('processamento-reap/<int:pk>/', views.ProcessamentoREAPdoAnoView.as_view(), name='processamento_reap_individual'),
    path('resetar-processamento/', views.resetar_processamento, name='resetar_processamento'),

]
