from django.urls import path
from . import views

# App Space Name
app_name = 'app_defeso'

urlpatterns = [
    
    path('defeso/lancamento/', views.DefesosLancamentoView.as_view(), name='lancamento_defeso'),
    path('controle/<int:pk>/edit/', views.ControleBeneficioEditView.as_view(), name='controle_beneficio_edit'),
]
