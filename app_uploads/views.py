# app_uploads/views.py

from core.views.base_imports import *
from core.views.app_uploads_imports import *
from core.choices import TIPO_MODELOS_MAP

class UploadsDocsCreateView(CreateView):
    model = UploadsDocs
    form_class = UploadsDocsForm
    template_name = 'uploads/uploads.html'

    def post(self, request, *args, **kwargs):
        tipos = request.POST.getlist('tipo')
        tipos_custom = request.POST.getlist('tipo_custom')
        arquivos = request.FILES.getlist('arquivo')
        instances = []

        content_type = request.GET.get('type')
        object_id = request.GET.get('id')

        tipo_tuple = TIPO_MODELOS_MAP.get(content_type.lower())
        if not tipo_tuple:
            raise Http404("Modelo inválido.")

        app_label, model_name = tipo_tuple
        ModelClass = apps.get_model(app_label=app_label, model_name=model_name)
        content_type_instance = ContentType.objects.get_for_model(ModelClass)

        for idx, arquivo in enumerate(arquivos):
            if not arquivo:
                continue
            tipo = TipoDocumentoUp.objects.filter(pk=tipos[idx]).first() if idx < len(tipos) and tipos[idx] else None
            tipo_custom = tipos_custom[idx] if idx < len(tipos_custom) else ''

            inst = UploadsDocs(
                tipo=tipo,
                tipo_custom=tipo_custom,
                arquivo=arquivo,
                enviado_por=request.user,
                proprietario_content_type=content_type_instance,
                proprietario_object_id=object_id,
            )
            inst.save()
            instances.append(inst)

        messages.success(request, f'{len(instances)} arquivo(s) enviados com sucesso!')
        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        content_type = self.request.GET.get('type')
        object_id = self.request.GET.get('id')

        # Verifica se temos um tipo conhecido no mapa
        if content_type and content_type.lower() in TIPO_MODELOS_MAP:
            tipo = content_type.lower()
            pk = object_id

            # Mapeamento dos nomes das views single por tipo
            if tipo == 'associado':
                url = reverse('app_associados:single_associado', kwargs={'pk': pk})
                return f"{url}#tab-uploads" 
            elif tipo == 'associacao':
                return reverse('app_associacao:single_associacao', kwargs={'pk': pk})
            elif tipo == 'reparticao':
                return reverse('app_associacao:single_reparticao', kwargs={'pk': pk})

        # fallback
        return reverse('app_home:home')



@login_required
def converter_para_pdf(request, pk):
    doc = get_object_or_404(UploadsDocs, pk=pk)
    ext = os.path.splitext(doc.arquivo.name)[1].lower()
    img_exts = {'.jpg', '.jpeg', '.png'}

    if ext not in img_exts:
        raise Http404("Apenas imagens podem ser convertidas")

    # Geração do PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.translate(0, height)
    img = Image.open(doc.arquivo)
    img_width, img_height = img.size
    ratio = min((width-72)/img_width, (height-72)/img_height)
    img_w, img_h = img_width*ratio, img_height*ratio
    x = (width - img_w) / 2
    y = -((height - img_h) / 2 + img_h)
    c.drawImage(doc.arquivo.path, x, y, img_w, img_h)
    c.showPage()
    c.save()

    buffer.seek(0)
    pdf_name = os.path.splitext(doc.arquivo.name)[0] + ".pdf"
    doc.arquivo.save(pdf_name, ContentFile(buffer.read()), save=False)
    doc.ext = "pdf"
    doc.save()

    messages.success(request, "Documento convertido com sucesso para PDF.")
    return redirect(f"{request.META.get('HTTP_REFERER', '/')}#tab-uploads")
