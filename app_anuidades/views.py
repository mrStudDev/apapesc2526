
# Views - App Anuidades
from core.views.base_imports import *
from core.views.app_anuidades_imports import *




class CreateAnuidadeView(CreateView):
    model = AnuidadeModel
    form_class = AnuidadeForm
    template_name = 'anuidades/create_anuidade.html'
    success_url = reverse_lazy('app_anuidades:list_anuidades')  # Ajuste para sua URL real

    def form_valid(self, form):
        # Salva a Anuidade primeiro
        anuidade = form.save(commit=False)
        anuidade.save()
        # Atribui a todos os associados ativos/aposentados, conforme regras
        anuidade.atribuir_anuidades_associados()
        messages.success(self.request, f"Anuidade de {anuidade.ano} criada e atribuída com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao Criar a Anuiade. Verifique os campos obrigatórios e o formato dos dados.')
        return super().form_invalid(form)    


class LancamentosAnuiadesListView(ListView)    :
    model = AnuidadeModel
    template_name = 'anuidades/list_anuidades.html'
    context_object_name = 'anuidades'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Total de anuidades
        context['qtd_anuidades'] = AnuidadeModel.objects.count()
        # Soma total dos valores
        context['valor_total_anuidades'] = AnuidadeModel.objects.aggregate(
            total=Sum('valor_anuidade')
        )['total'] or 0
        return context    



class AnuidadeAssociadoSingleView(DetailView):
    model = AssociadoModel
    template_name = 'anuidades/anuidade_associado.html'
    context_object_name = 'associado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        associado = self.object
        anuidades = AnuidadeAssociado.objects.filter(associado=associado).select_related('anuidade').order_by('-anuidade__ano')

        # TOTAIS GLOBAIS
        total_pago_geral = Decimal('0.00')
        total_descontos_geral = Decimal('0.00')
        saldo_devedor_geral = Decimal('0.00')
        
        anuidade_infos = []
        for aa in anuidades:
            pagamentos = aa.pagamentos.order_by('-data_pagamento')
            descontos = aa.descontos.order_by('-data_concessao')

            total_pago = pagamentos.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
            total_descontos = descontos.aggregate(total=Sum('valor_desconto'))['total'] or Decimal('0.00')
            valor_anuidade = aa.anuidade.valor_anuidade
            saldo_devedor = max(valor_anuidade - total_descontos - total_pago, Decimal('0.00'))
            status = "PAGA" if saldo_devedor <= 0 else "EM ABERTO"

            # Somando nos totais GERAIS
            total_pago_geral += total_pago
            total_descontos_geral += total_descontos
            saldo_devedor_geral += saldo_devedor

            anuidade_infos.append({
                'aa': aa,
                'pagamentos': pagamentos,
                'descontos': descontos,
                'total_pago': total_pago,
                'total_descontos': total_descontos,
                'valor_anuidade': valor_anuidade,
                'saldo_devedor': saldo_devedor,
                'status_anuidade': status,
                'pagamento_form': PagamentoForm(),
                'desconto_form': DescontoAnuidadeForm(),
            })

        context['anuidade_infos'] = anuidade_infos
        context['total_pago_geral'] = total_pago_geral
        context['total_descontos_geral'] = total_descontos_geral
        context['saldo_devedor_geral'] = saldo_devedor_geral
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        associado = self.object
        anuidades = AnuidadeAssociado.objects.filter(associado=associado)
        
        anuidade_id = request.POST.get('anuidade_id')
        aa = anuidades.get(pk=anuidade_id)

        if 'pagar' in request.POST:
            form = PagamentoForm(request.POST, request.FILES)
            if form.is_valid():
                pagamento = Pagamento.objects.create(
                    anuidade_associado=aa,
                    valor=form.cleaned_data['valor'],
                    registrado_por=request.user,
                    comprovante_up=form.cleaned_data.get('comprovante_up')
                )
                aa.atualizar_status_pagamento()
                
        elif 'descontar' in request.POST:
            form = DescontoAnuidadeForm(request.POST)
            if form.is_valid():
                desconto = form.save(commit=False)
                desconto.anuidade_associado = aa
                desconto.concedido_por = request.user
                desconto.save()
                aa.atualizar_status_pagamento()
                
        return redirect(reverse('app_anuidades:anuidade_associado_singular', args=[associado.pk]))
