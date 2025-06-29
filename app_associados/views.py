# Views App Associados
from core.views.base_imports import *
from core.views.app_associados_imports import *


# CREATES ==================================================================
class AssociadoCreateView(LoginRequiredMixin, CreateView):
    model = AssociadoModel
    form_class = AssociadoForm
    template_name = 'associados/create_associado.html'

    def dispatch(self, request, *args, **kwargs):
        # Verifica se o usuário tem permissão para criar um associado
        if not (request.user.is_authenticated and (request.user.is_superuser or request.user.user_type == 'admin_associacao')):
            messages.error(self.request, "Você não tem permissão para criar um associado.")
            return redirect('app_accounts:unauthorized')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.GET.get('user_id') or None
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            kwargs['user_initial'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associacao_id = self.request.GET.get('associacao_id')
        user_id = self.request.GET.get('user_id')

        if associacao_id:
            from app_associacao.models import AssociacaoModel
            context['associacao_obj'] = get_object_or_404(AssociacaoModel, pk=associacao_id)

        if user_id:
            context['user_obj'] = get_object_or_404(CustomUser, pk=user_id)

        return context

    def form_valid(self, form):
        # Verifica se o usuário foi passado e associa ao associado
        user_id = self.request.GET.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            form.instance.user = user  # Associa o usuário ao associado

            # Atualiza o e-mail do usuário, se for diferente
            user_email = form.cleaned_data.get('email')
            if user_email and user.email != user_email:
                user.email = user_email
                user.save()
        else:
            messages.error(self.request, "⚠️ Erro: Nenhum usuário selecionado para associação.")
            return self.form_invalid(form)

        # Salva o associado
        self.object = form.save()

        messages.success(self.request, "✅ Associado salvo com sucesso!")

        # Redireciona baseado no botão clicado
        if "save_and_continue" in self.request.POST:
            return redirect(reverse('app_associados:edit_associado', kwargs={'pk': self.object.pk}))
        elif "save_and_view" in self.request.POST:
            return redirect(reverse('app_associados:edit_associado', kwargs={'pk': self.object.pk}))

        return super().form_valid(form)
    
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar o Associado. Verifique os campos obrigatórios.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app_associados:edit_associado', kwargs={'pk': self.object.pk})

# -----------------------------------------------------------------------------------------
# SINGLES =================================================================================
class AssociadoSingleView(LoginRequiredMixin, DetailView):
    model = AssociadoModel
    template_name = 'associados/single_associado.html'
    context_object_name = 'associado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 📦 Importante: filtramos pelo ContentType genérico
        from django.contrib.contenttypes.models import ContentType
        from app_uploads.models import UploadsDocs

        associado = self.object
        content_type = ContentType.objects.get_for_model(AssociadoModel)

        # Lista todos os uploads ligados a este associado
        uploads = UploadsDocs.objects.filter(
            proprietario_content_type=content_type,
            proprietario_object_id=associado.pk
        ).order_by('tipo__nome')

        context['uploads_docs'] = uploads
        return context

# -----------------------------------------------------------------------------------------

# EDITS ================================================================

class AssociadoUpdateView(LoginRequiredMixin, UpdateView):
    model = AssociadoModel
    form_class = EditAssociadoForm
    template_name = 'associados/edit_associado.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.GET.get('user_id') or None
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            kwargs['user_initial'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associacao_id = self.request.GET.get('associacao_id')
        reparticao_id = self.request.GET.get('reparticao_id')
        user_id = self.request.GET.get('user_id')
        
        associado = self.get_object()
        user = associado.user 
        
        if associacao_id:
            from app_associacao.models import AssociacaoModel
            context['associacao_obj'] = get_object_or_404(AssociacaoModel, pk=associacao_id)

        if reparticao_id:
            from app_associacao.models import ReparticoesModel
            context['reparticao_obj'] = get_object_or_404(AssociacaoModel, pk=reparticao_id)


        if user_id:
            context['user_obj'] = get_object_or_404(CustomUser, pk=user_id)

        context['user_obj'] = user

        return context
        
    def form_valid(self, form):
        # Quando o formulário for validado, salva as alterações
        response = super().form_valid(form)
        
        user_id = self.request.GET.get('user_id')
        if user_id:
            user = get_object_or_404(CustomUser, pk=user_id)
            form.instance.user = user  # Associa o usuário ao associado

        # 🧠 Agora processamos manualmente os ManyToMany
        petrechos_ids = self.request.POST.getlist('petrechos_pesca')
        if petrechos_ids:
            self.object.petrechos_pesca.set(petrechos_ids)
        else:
            self.object.petrechos_pesca.clear()

            
        messages.success(self.request, 'Associado atualizado com sucesso!')
        return response

    def form_invalid(self, form):
        # Em caso de erro, exibe uma mensagem
        messages.error(self.request, 'Erro ao salvar o Associado. Verifique os campos obrigatórios.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('app_associados:single_associado', kwargs={'pk': self.object.pk})
    
# ---------------------------------------------------------------------------------    

# LISTS ==========================================================================
class AssociadoListView(LoginRequiredMixin, ListView):
    model = AssociadoModel
    template_name = 'associados/list_associados.html'
    context_object_name = 'associados'



class AssociadoHistoricoView(DetailView):
    model = AssociadoModel
    template_name = 'associados/historico_associado.html'
    context_object_name = 'associado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associado = self.get_object()
        historico = list(associado.history.all().order_by('-history_date'))

        diffs = []

        for i in range(len(historico) - 1):
            current = historico[i]
            previous = historico[i + 1]
            delta = current.diff_against(previous)
            diffs.append({
                'entry': current,
                'changes': delta.changes,
            })

        # Add final entry (sem comparação possível)
        if historico:
            diffs.append({
                'entry': historico[-1],
                'changes': [],
            })

        context['diffs'] = diffs
        return context
    

# app_associados
class EnviarParaDriveView(View):
    def post(self, request, pk):
        doc = get_object_or_404(UploadsDocs, pk=pk)

        # Verifica se tem pasta associada
        prop = doc.proprietario_object
        folder_id = getattr(prop, 'drive_folder_id', None)

        if not folder_id:
            messages.error(request, "Este associado não possui pasta no Drive.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            upload_file_to_drive(doc.arquivo.path, doc.arquivo.name, folder_id)
            messages.success(request, "Arquivo enviado para o Google Drive com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao enviar para o Drive: {e}")

        return redirect(request.META.get('HTTP_REFERER', '/'))    
    


def upload_file_to_drive(filepath, filename, parent_folder_id):
    service = get_drive_service()

    file_metadata = {
        'name': filename,
        'parents': [parent_folder_id]
    }

    media = MediaFileUpload(filepath, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    return uploaded_file.get('id')

