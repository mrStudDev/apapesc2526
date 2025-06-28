# app_uploads/urls.py
from django.urls import path
from .views import UploadsDocsCreateView
from . import views

app_name = "app_uploads"

urlpatterns = [
    path('novo/', UploadsDocsCreateView.as_view(), name='create_upload'),
    path('converter-pdf/<uuid:pk>/', views.converter_para_pdf, name='converter_para_pdf'),
]