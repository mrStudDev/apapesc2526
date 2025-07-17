# Models App Serviços
from django.db import models
from decimal import Decimal
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.utils import timezone
from django.db.models import Sum, Q
from django.utils.timezone import now
from app_associacao.models import AssociacaoModel, ReparticoesModel
from app_associados.models import AssociadoModel
from django.conf import settings

from core.choices import (
    NATUREZA_SERVICO_CHOICES,
    TIPO_SERVICO,
    STATUS_EMISSAO_DOC,
    STATUS_CONSULTORIA,
    STATUS_ASSESSORIA_PROCESSO,
    FORMA_PAGAMENTO_CHOICES,
    PARCELAMENTO_CHOICES,
    STATUS_PAGAMENTO_CHOICES,
    STATUS_COBRANCA
)


# Serviço associado
class ServicoModel(models.Model):

    natureza_servico = models.CharField(
        max_length=100,
        choices=NATUREZA_SERVICO_CHOICES,
        verbose_name="Natureza do Serviço"
    )          
    tipo_servico = models.CharField(
        max_length=100,
        choices=TIPO_SERVICO,
        verbose_name="Tipo Serviço"
    )      
    # Vínculo
    associacao = models.ForeignKey(
        AssociacaoModel, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        related_name='servicos_associacao',
        verbose_name="Associação"
    )
    reparticao = models.ForeignKey(
        ReparticoesModel, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True, 
        related_name='servicos_reparticao',
        verbose_name="Repartição"
    )    

    # 🔹 Só um desses será preenchido
    associado = models.ForeignKey(
        AssociadoModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Associado"
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    data_inicio = models.DateTimeField(auto_now_add=True)
    
    status_servico = models.CharField(
        max_length=40,
        verbose_name="Status do Serviço"
    )    
    content = models.TextField(blank=True, null=True)

    ultima_alteracao = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='servicos_criados',
        null=True,
        blank=True,
        verbose_name="Criado por"
    )
          
    history = HistoricalRecords()      

    def precisa_entrada_financeira(self):
        # Se não houver associado, nunca gera cobrança
        if not self.associado or not self.associado.status:
            return False
        return self.associado.status in STATUS_COBRANCA
    
    def clean(self):
            from django.core.exceptions import ValidationError

            status_choices = {
                'assessoria': dict(STATUS_ASSESSORIA_PROCESSO),
                'consultoria': dict(STATUS_CONSULTORIA),
                'emissao_documento': dict(STATUS_EMISSAO_DOC),
            }
            if self.natureza_servico not in status_choices:
                raise ValidationError('Natureza do serviço inválida.')

            valid_status = status_choices[self.natureza_servico]
            if self.status_servico and self.status_servico not in valid_status:
                raise ValidationError(f'Status "{self.status_servico}" não permitido para {self.natureza_servico}.')    
         
    def __str__(self):
        return f"{self.associado} - {self.natureza_servico}"            


class EntradaFinanceiraModel(models.Model):
    servico = models.OneToOneField(
        ServicoModel,
        on_delete=models.CASCADE,
        related_name='entrada_servico'
    )
    forma_pagamento = models.CharField(max_length=10, choices=FORMA_PAGAMENTO_CHOICES, verbose_name="Forma de Pagamento")
    parcelamento = models.CharField(max_length=15, choices=PARCELAMENTO_CHOICES, verbose_name="Parcelamento")
    status_pagamento = models.CharField(max_length=10, choices=STATUS_PAGAMENTO_CHOICES, default="pendente", verbose_name="Status do Pagamento", editable=False)
        
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_entrada = models.DateTimeField(auto_now_add=True)
    pago = models.BooleanField(default=False)

    valor_pagamento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),  # 🔥 Usa Decimal para evitar erros
        blank=True,
        null=True,
        verbose_name="Valor Pago"
    )    

    def __str__(self):
        return f"Entrada {self.valor} para Serviço {self.servico.id}"
            
    def calcular_pagamento(self):
        """ Atualiza o valor restante e o status do pagamento. """
        total_pago = self.servico.pagamentos.aggregate(total=Sum("valor_pago"))["total"] or Decimal('0.00')
        
        # Atualiza o valor do campo "valor_pagamento"
        self.valor_pagamento = total_pago

        # Atualiza status com base no saldo restante
        saldo_restante = self.valor - total_pago
        if saldo_restante <= Decimal('0.00'):
            self.status_pagamento = "pago"
        elif total_pago > Decimal('0.00'):
            self.status_pagamento = "parcial"
        else:
            self.status_pagamento = "pendente"

        self.save(update_fields=["valor_pagamento", "status_pagamento"])


    def clean(self):
        super().clean()
        # Só faz a validação se self.servico já existe!
        if self.servico_id and self.servico:
            if not self.servico.precisa_entrada_financeira():
                from django.core.exceptions import ValidationError
                raise ValidationError("Só é permitido criar entrada financeira para serviços de extra associados, cliente especial ou desassociado.")


class PagamentoEntrada(models.Model):
    servico = models.ForeignKey(ServicoModel, on_delete=models.CASCADE, related_name="pagamentos")
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    data_pagamento = models.DateTimeField(default=now)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Registrado por"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 🔥 Após registrar o pagamento, recalcula o status da entrada
        entrada = self.entrada
        if entrada:
            entrada.calcular_pagamento()

    @property
    def entrada(self):
        # Retorna a entrada financeira do serviço
        return getattr(self.servico, 'entrada_servico', None)

        
    def __str__(self):
        return f"Pagamento de R$ {self.valor_pago} em {self.data_pagamento.strftime('%d/%m/%Y')} - Entrada {self.servico.id}"
            