# app_uploads/urls.py
from django.urls import path
from .views import UploadsDocsCreateView
from . import views

app_name = "app_uploads"

urlpatterns = [
    path('novo/', UploadsDocsCreateView.as_view(), name='create_upload'),
    path('tipo-documento/novo/', views.TipoDocumentoCreateView.as_view(), name='create_tipo_doc'),
    path('lista-tipos/', views.TipoDocumentoLstView.as_view(), name='list_tipo_docs'),
    path('editar-tipo-doc/<int:pk>', views.TipoDocumentoEditView.as_view(), name='edit_tipo_doc'),
    path('deletar-tipo-doc/<int:pk>/', views.TipoDocumentoDeleteView.as_view(), name='delete_tipo_doc'),
    path('delete/<uuid:pk>/', views.delete_upload, name='delete_upload'),

    # Corverter
    path('converter-pdf/<uuid:pk>/', views.converter_para_pdf, name='converter_para_pdf'),

]