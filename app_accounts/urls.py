from django.urls import path
from . import views
from allauth.account.views import LoginView, LogoutView

app_name = 'app_accounts'

urlpatterns = [
    path('dashboards/', views.dashboard, name='dashboard_superuser'),
    path('dashboards/', views.dashboard, name='admin_geral'),


    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    

]