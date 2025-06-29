# app_uploads/forms.py
from django import forms
from .models import UploadsDocs, TipoDocumentoUp

    
    
class UploadsDocsForm(forms.ModelForm):
    arquivo = forms.FileField(label="Arquivo")

    class Meta:
        model = UploadsDocs
        fields = ['tipo', 'tipo_custom', 'arquivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordena o queryset do campo tipo
        self.fields['tipo'].queryset = TipoDocumentoUp.objects.all().order_by('nome')
        
    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        tipo_custom = cleaned_data.get('tipo_custom')

        if not tipo and not tipo_custom:
            raise forms.ValidationError("Preencha o tipo ou digite uma classificação.")
        return cleaned_data

class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumentoUp
        fields = ['nome', 'descricao']