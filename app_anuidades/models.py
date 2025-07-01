from django.shortcuts import render
from django.contrib.auth.models import User 
from django.db import models, transaction
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP, ROUND_DOWN
from app_associados.models import AssociadoModel, AssociacaoModel
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Sum, Q
from django.apps import apps 
from django.conf import settings
from django.db.models.functions import Lower
from django.forms.models import model_to_dict
from datetime import datetime
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


# Anuidade Geral - Todos Associados e Associações.
class AnuidadeModel(models.Model):
    ano = models.PositiveIntegerField(unique=True, verbose_name="Ano da Anuidade")
    valor_anuidade = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor da Anuidade")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ano']
        verbose_name = "Anuidade"
        verbose_name_plural = "Anuidades"

    def __str__(self):
        return f"Anuidade {self.ano} - R$ {self.valor_anuidade}"

    def save(self, *args, **kwargs):
        """
        Ao salvar a anuidade, atribuir a todos os associados existentes.
        """
        super().save(*args, **kwargs)

    def atribuir_anuidades_associados(self):
        """
        Atribui esta anuidade somente aos associados ATIVOS ou APOSENTADOS
        que já estavam filiados no ano da anuidade (ou antes).
        """
        AssociadoModel = apps.get_model('app_associados', 'AssociadoModel')
        AnuidadeAssociado = apps.get_model('app_anuidades', 'AnuidadeAssociado')

        associados = AssociadoModel.objects.annotate(
            status_lower=Lower('status')
        ).filter(
            status_lower__in=['associado_lista_ativo', 'associado_lista_aposentado'],
            data_filiacao__isnull=False,
            data_filiacao__year__lte=self.ano  # ✅ Associado já existia no ano da anuidade
        )

        if not associados.exists():
            print(f"⚠️ Nenhum associado estava filiado no ano {self.ano}, nenhuma aplicação feita.")
            return

        print(f"✅ Aplicando anuidade {self.ano} para {associados.count()} associados...")

        with transaction.atomic():
            for associado in associados:
                if not AnuidadeAssociado.objects.filter(anuidade=self, associado=associado).exists():
                    AnuidadeAssociado.objects.create(
                        anuidade=self,
                        associado=associado,
                        valor_pago=Decimal('0.00'),
                        pago=False
                    )

    def calcular_meses_validos(self, associado):
        """
        Calcula o número de meses para o cálculo pró-rata
        com base em associado.data_filiacao e self.ano.
        """
        if not associado.data_filiacao or associado.data_filiacao.year > self.ano:
            print(f"⚠️ Nenhum mês válido para {associado} - Data de Filiação: {associado.data_filiacao}, Anuidade: {self.ano}")
            return 0

        if associado.data_filiacao.year == self.ano:
            meses = 12 - associado.data_filiacao.month + 1
            print(f"✅ Cálculo pró-rata para {associado}: {meses} meses")  # DEBUG
            return meses
        
        print(f"✅ Anuidade completa para {associado}")
        return 12  # Se a filiação foi antes do ano da anuidade, paga o valor total

    def qtd_anuidades(self):
        return self.anuidades_associados.count()

    def valor_total_anuidades(self):
        return self.qtd_anuidades() * self.valor_anuidade

# Anuidade Associado - Singular    
class AnuidadeAssociado(models.Model):
    anuidade = models.ForeignKey(AnuidadeModel, on_delete=models.CASCADE, related_name='anuidades_associados')
    associado = models.ForeignKey(
        'app_associados.AssociadoModel',
        on_delete=models.CASCADE,
        related_name='anuidades_associados'
    )
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor Pago")
    pago = models.BooleanField(default=False, verbose_name="Anuidade Paga")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anuidade', 'associado')
        ordering = ['associado']
        verbose_name = "Anuidade do Associado"
        verbose_name_plural = "Anuidades dos Associados"

    def __str__(self):
        return f"Anuidade {self.anuidade.ano} - {self.associado}"

    def calcular_saldo(self):
        """Calcula o saldo devedor da anuidade."""
        return max(self.anuidade.valor_anuidade - self.valor_pago, Decimal('0.00')) 


    def dar_baixa(self, valor_baixa):
        """Dá baixa parcial ou total no valor da anuidade."""
        self.valor_pago += valor_baixa
        if self.valor_pago >= self.anuidade.valor_anuidade:
            self.pago = True
        self.save()    

    def atualizar_status_pagamento(self):
        # Soma todos pagamentos e descontos
        total_pago = self.pagamentos.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        total_descontos = self.descontos.aggregate(total=Sum('valor_desconto'))['total'] or Decimal('0.00')
        valor_total = total_pago + total_descontos
        if valor_total >= self.anuidade.valor_anuidade:
            self.pago = True
        else:
            self.pago = False
        self.valor_pago = total_pago
        self.save(update_fields=['pago', 'valor_pago'])

# Pagamento de uma Anuidade
class Pagamento(models.Model):
    anuidade_associado = models.ForeignKey(AnuidadeAssociado, on_delete=models.CASCADE, related_name='pagamentos', default=None)
    data_pagamento = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Pago")
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Registrado por"
    )
    comprovante_up = models.FileField(
        upload_to='comprovantes_anuidades/',
        null=True, blank=True,
        verbose_name="Comprovante do Pagamento"
    )
    
    def __str__(self):
        return f"Pagamento de R$ {self.valor} em {self.data_pagamento}"

    def clean(self):
        super().clean()

        # 🔍 Obtem os valores atuais
        total_descontos = self.anuidade_associado.descontos.aggregate(
            total=models.Sum('valor_desconto')
        )['total'] or Decimal('0.00')

        total_pagamentos = self.anuidade_associado.pagamentos.aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0.00')

        # 🔥 Se está editando o próprio pagamento, remove ele do total
        if self.pk:
            total_pagamentos -= Pagamento.objects.filter(pk=self.pk).values_list('valor', flat=True).first() or Decimal('0.00')

        # ⚠️ Verificar o limite permitido
        valor_anuidade = self.anuidade_associado.anuidade.valor_anuidade
        valor_disponivel = valor_anuidade - total_descontos - total_pagamentos

        if self.valor > valor_disponivel:
            raise ValidationError(
                f"Valor excede o limite permitido. Anuidade: R$ {valor_anuidade}, "
                f"Desconto aplicado: R$ {total_descontos}, "
                f"Já pago: R$ {total_pagamentos}. "
                f"Disponível para pagamento: R$ {valor_disponivel}."
            )

    def save(self, *args, **kwargs):
        self.clean()  # ✔️ Executa a validação antes de salvar
        super().save(*args, **kwargs)        
        

# Desconto de anuidades.
class DescontoAnuidade(models.Model):
    anuidade_associado = models.ForeignKey(
        AnuidadeAssociado,
        on_delete=models.CASCADE,
        related_name="descontos",
        verbose_name="Anuidade Associado"
    )
    valor_desconto = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor do Desconto"
    )
    motivo = models.CharField(max_length=1000, verbose_name="Motivo do Desconto")

    concedido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Concedido por"
    )    
    data_concessao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Desconto na Anuidade"
        verbose_name_plural = "Descontos nas Anuidades"

    def __str__(self):
        return f"Desconto de R$ {self.valor_desconto} para {self.anuidade_associado}"        
    
    def clean(self):
        super().clean()
        if self.anuidade_associado and self.anuidade_associado.pago:
            raise ValidationError("Não é permitido lançar desconto em anuidade já quitada!")
        