from core.views.base_imports import *
from core.views.app_reap_imports import *

class LancamentosREAPListView(ListView):
    model = REAPdoAno
    template_name = 'reap/lancamentos_reap.html'
    context_object_name = 'reaps'
    paginate_by = 30

    def get_queryset(self):
        ano = self.request.GET.get('ano') or timezone.now().year
        return REAPdoAno.objects.filter(ano=ano)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ano = int(self.request.GET.get('ano', timezone.now().year))
        rodada = REAPdoAno.objects.filter(ano=ano).aggregate(Max('rodada'))['rodada__max'] or 1
        tem_processamento = REAPdoAno.objects.filter(
            ano=ano, rodada=rodada, em_processamento_por__isnull=False
        ).exists()

        # Para popular um seletor de anos (últimos 4 anos, por exemplo)
        context['anos'] = range(2022, timezone.now().year + 2)
        context['ano_selecionado'] = ano
        context['rodada'] = rodada
        context['tem_processamento'] = tem_processamento
        return context

    def post(self, request, *args, **kwargs):
        ano = int(request.POST.get('ano') or timezone.now().year)
        criados = criar_reap_do_ano(ano)
        if criados:
            messages.success(request, f"{criados} lançamentos REAP criados para {ano}.")
        else:
            messages.info(request, f"Nenhum novo REAP foi criado para {ano} (já existem para todos).")
        # Redireciona para manter GET params
        return redirect(f"{request.path}?ano={ano}")
    
    

class ProcessamentoREAPdoAnoView(LoginRequiredMixin, View):
    template_name = 'reap/processamento_manual_reap.html'

    def get(self, request):
        ano = request.GET.get('ano')
        if not ano:
            messages.error(request, "Selecione o ano primeiro.")
            return redirect('app_reap:lancamentos_reap')
        ano = int(ano)

        # Descobre a última rodada
        ult_rodada = REAPdoAno.objects.filter(ano=ano).aggregate(Max('rodada'))['rodada__max']
        if ult_rodada is None:
            messages.error(request, "Não há registros REAP para este ano.")
            messages.warning(request, "Você precisa criar os lançamentos REAP deste ano antes de processar!")
            return redirect('app_reap:lancamentos_reap')

        abertas = REAPdoAno.objects.filter(ano=ano, rodada=ult_rodada, processada=False).exists()
        if abertas:
            rodada = ult_rodada
        else:
            messages.info(request, "Todos os REAP deste ano já foram processados. Inicie uma nova rodada se desejar.")
            return redirect('app_reap:lancamentos_reap')

        processamento, _ = ProcessamentoREAPModel.objects.get_or_create(
            ano=ano, rodada=rodada, usuario=request.user,
            defaults={'status': 'usuario_processando'}
        )

        reap = REAPdoAno.objects.filter(
            ano=ano, rodada=rodada, processada=False, em_processamento_por=request.user
        ).first()
        if not reap:
            reap = pegar_proximo_reap_para_usuario(ano, rodada, request.user)

        if not reap:
            processamento.status = 'Processada'
            processamento.concluido_em = timezone.now()
            processamento.save()
            checar_e_apagar_processamento(ano, rodada)
            return redirect('app_reap:lancamentos_reap')

        total_reaps = REAPdoAno.objects.filter(ano=ano, rodada=rodada).count()

        # Descobrir o índice do REAP atual (1-based!)
        if reap:
            reaps_ordenados = list(REAPdoAno.objects.filter(ano=ano, rodada=rodada).order_by('associado__user', 'id'))
            reap_index = reaps_ordenados.index(reap) + 1
        else:
            reap_index = None

        usuarios_em_processamento = REAPdoAno.objects.filter(
            ano=ano, rodada=rodada, em_processamento_por__isnull=False
        ).values_list('em_processamento_por__username', flat=True).distinct()

        return render(request, self.template_name, {
            'reap': reap,
            'processamento': processamento,
            'ano': ano,
            'rodada': rodada,
            'STATUS_RESPOSTAS_REAP': STATUS_RESPOSTAS_REAP,
            'total_reaps': total_reaps,
            'reap_index': reap_index,
            'usuarios_em_processamento': usuarios_em_processamento,
        })

    def post(self, request):
        ano = int(request.GET.get('ano'))
        rodada = int(request.GET.get('rodada', 1))
        reap_id = request.POST.get('reap_id')

        reap = REAPdoAno.objects.get(id=reap_id)
        reap.status_resposta = request.POST.get('status_resposta', reap.status_resposta)
        reap.save()

        action = request.POST.get('action', 'proximo')

        if action == "voltar":
            messages.success(request, "Alterações salvas! Você pode retomar o processamento depois.")
            return redirect('app_reap:lancamentos_reap')

        # Se for "proximo" (default), segue fluxo normal:
        reap.processada = True
        reap.em_processamento_por = None
        reap.save(update_fields=['processada', 'em_processamento_por'])

        proximo_reap = pegar_proximo_reap_para_usuario(ano, rodada, request.user)
        if not proximo_reap:
            checar_e_apagar_processamento(ano, rodada)
            return redirect('app_reap:lancamentos_reap')

        processamento = ProcessamentoREAPModel.objects.get(
            ano=ano, rodada=rodada, usuario=request.user
        )

        total_reaps = REAPdoAno.objects.filter(ano=ano, rodada=rodada).count()
        reaps_ordenados = list(REAPdoAno.objects.filter(ano=ano, rodada=rodada).order_by('associado__user', 'id'))
        reap_index = reaps_ordenados.index(proximo_reap) + 1

        usuarios_em_processamento = REAPdoAno.objects.filter(
            ano=ano, rodada=rodada, em_processamento_por__isnull=False
        ).values_list('em_processamento_por__username', flat=True).distinct()

        return render(request, self.template_name, {
            'reap': proximo_reap,
            'processamento': processamento,
            'ano': ano,
            'rodada': rodada,
            'STATUS_RESPOSTAS_REAP': STATUS_RESPOSTAS_REAP,
            'total_reaps': total_reaps,
            'reap_index': reap_index,
            'usuarios_em_processamento': usuarios_em_processamento,
        })
        
    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        ano = request.GET.get('ano') or str(timezone.now().year)

        context['ano_selecionado'] = str(ano)
        return context
    
@require_POST
@login_required
def resetar_processamento(request):
    ano = int(request.GET.get('ano'))
    rodada = REAPdoAno.objects.filter(ano=ano).aggregate(Max('rodada'))['rodada__max'] or 1

    qs = REAPdoAno.objects.filter(ano=ano, rodada=rodada)
    # Aqui reseta só os campos de processamento!
    updated = qs.update(processada=False, em_processamento_por=None)
    messages.success(request, f"{updated} guias resetadas para {ano}, rodada {rodada}!")
    return redirect(f"{reverse('app_reap:lancamentos_reap')}?ano={ano}")