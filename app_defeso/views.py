from core.views.base_imports import *
from core.views.app_defeso_imports import *

class DefesosLancamentoView(View):
    template_name = 'defeso/defesos.html'

    def get(self, request):
        beneficio_id = request.GET.get('beneficio')
        beneficios = SeguroDefesoBeneficioModel.objects.all().order_by('-ano_concessao', '-data_inicio')
        associados_beneficiados = []

        if beneficio_id:
            associados_beneficiados = ControleBeneficioModel.objects.filter(
                beneficio_id=beneficio_id
            ).select_related('associado')

        return render(request, self.template_name, {
            'beneficios': beneficios,
            'beneficio_id': beneficio_id,
            'associados_beneficiados': associados_beneficiados,
        })
        

class ControleBeneficioEditView(UpdateView):
    model = ControleBeneficioModel
    form_class = ControleBeneficioForm
    template_name = 'defeso/controle_beneficio_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        controle = self.object
        associado = controle.associado

        # DOCUMENTOS ESSENCIAIS E RELACIONADOS
        tipos_doc_essencial = [
            '001_Auto_Declaração_Pesca', 
            '002_Autorização_ACESSO_GOV_ASS_Associado',  
            '003_Autorização_IMAGEM_ASS_Associado',   
            '004_CAEPF',  
            '005_CEI',  
            '006_CNH_Cart_Motorista',  
            '007_Comp_Resid_LUZ_AGUA_FATURAS',  
            '008_Comp_SEGURO_DEFESO',  
            '009_CPF_Pessoa_Física',  
            '0010_CTPS_Cart_Trabalho', 
            '0011_Declaração_Residência_MAPA',  
            '0012_Ficha_Req_Filiação_ASS_PRESID_JUR', 
            '0013_Ficha_Req_Filiação_ASS_Associado',  
            '0014_Foto_3x4', 
            '0015_Licença_Embarcação',  
            '0016_NIT_Extrato',  
            '0017_Procuração_AD_JUDICIA',  
            '0018_Procuracao_ADMINISTRATIVA',  
            '0019_Protocolo_ENTRADA_RGP',  
            '0020_RG_Identidade_CIN',
            '0021_RGP_Cart_Pescador',
            '0021_TIE_Titulo_Embarcação',
            '0022_Titulo_Eleitor',
        ]

        # Pegue todos uploads do associado
        from app_uploads.models import UploadsDocs  # ajuste para o seu path real!
        documentos_up = UploadsDocs.objects.filter(
            proprietario_object_id=associado.pk,
            proprietario_content_type=ContentType.objects.get_for_model(type(associado)),
            tipo__nome__in=tipos_doc_essencial
        ).select_related('tipo')

        context['documentos_essenciais_up'] = documentos_up
        return context


    def get_success_url(self):
        # Redireciona de volta para a tela de lista ou detalhe, ajuste conforme seu fluxo!
        return reverse_lazy('app_defeso:lancamento_defeso')        