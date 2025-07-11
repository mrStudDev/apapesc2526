from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from app_associados.models import AssociadoModel
from django.db import transaction
import threading
import time

from core.choices import(
    STATUS_PROCESSAMENTO,
    STATUS_RESPOSTAS_REAP
)

class REAPdoAno(models.Model):
    associado = models.ForeignKey(
        'app_associados.AssociadoModel',
        on_delete=models.CASCADE,
        related_name='reap_anual'
    )
    ano = models.PositiveIntegerField()
    status_resposta = models.CharField(
        max_length=12, choices=STATUS_RESPOSTAS_REAP, default='pendente'
    )    
    atualizado_em = models.DateTimeField(auto_now=True)    
    processada = models.BooleanField(default=False)
    rodada = models.PositiveIntegerField(null=True, blank=True, default=1)
    em_processamento_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='reap_anual_em_processamento'
    )    
    history = HistoricalRecords()

    class Meta:
        unique_together = ('associado', 'ano', 'rodada')
        ordering = ['-ano', 'associado']

    def __str__(self):
        return f"{self.associado} - {self.ano}"
    
    @property
    def nome_reap(self):
        return f"reap_ano_{self.ano}"
    
    
def criar_reap_do_ano(ano, rodada=1):
    ativos_aposentados = AssociadoModel.objects.filter(
        status__in=['associado_lista_ativo', 'associado_lista_aposentado'],
    )
    criados = 0
    for associado in ativos_aposentados:
        reap, created = REAPdoAno.objects.get_or_create(
            associado=associado,
            ano=ano,
            rodada=rodada,
            defaults={'status_resposta': 'pendente'}
        )
        if created:
            criados += 1
    return criados  
  

class ProcessamentoREAPModel(models.Model):
    ano = models.PositiveIntegerField()
    rodada = models.PositiveIntegerField(default=1)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processamentos_reap'
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_PROCESSAMENTO,
        default='usuario_processando'
    )
    iniciado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    concluido_em = models.DateTimeField(null=True, blank=True)
    indice_atual = models.PositiveIntegerField(default=0)
    total_associados = models.PositiveIntegerField(default=0)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('ano', 'rodada', 'usuario')
        ordering = ['-iniciado_em']

    def __str__(self):
        return f"Processamento REAP {self.ano} - {self.usuario} (Rodada {self.rodada})"
    
    
def pegar_proximo_reap_para_usuario(ano, rodada, usuario):
    with transaction.atomic():
        # tenta encontrar reap em aberto não processada e não em processamento
        reap = REAPdoAno.objects.select_for_update(skip_locked=True).filter(
            ano=ano,
            rodada=rodada,
            processada=False,
            em_processamento_por__isnull=True
        ).first()
        if reap:
            reap.em_processamento_por = usuario
            reap.save(update_fields=['em_processamento_por'])
            return reap
        # se não há nenhuma, retorna None
        return None  
    


def checar_e_apagar_processamento(ano, rodada):
    restantes = REAPdoAno.objects.filter(
        ano=int(ano), rodada=int(rodada), processada=False
    ).exists()
    if not restantes:
        def apagar():
            print('### Apagando processamento da rodada:', ano, rodada)
            time.sleep(2)
            deleted, _ = ProcessamentoREAPModel.objects.filter(
                ano=int(ano), rodada=int(rodada)
            ).delete()
            print('Processamento apagado? Quantos:', deleted)
            REAPdoAno.objects.filter(
                ano=int(ano), rodada=int(rodada)
            ).update(em_processamento_por=None)
            print('Locks de reaps limpos!')
        threading.Thread(target=apagar).start()
        return True
    return False    