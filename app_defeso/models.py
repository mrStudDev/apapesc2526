from django.db import models
from datetime import date
from django.utils.text import slugify
from app_associados.models import AssociadoModel
import os
from simple_history.models import HistoricalRecords

from core.choices import(
    UF_CHOICES,
    TIPO_ATO_NORMATIVO_CHOICES,
    STATUS_BENEFICIO_CHOICES
)




class LeiFederalPrevidenciaria(models.Model):
    """
    Modelo para armazenar informações sobre Leis Federais Previdenciárias.
    Ex: Lei nº 10.779/2003 (principal lei do Seguro Defeso)
    """
    numero = models.CharField(max_length=50, unique=True, help_text="Número da Lei (Ex: 10.779/2003)")
    ementa = models.TextField(blank=True, null=True, help_text="Ementa da Lei")
    data_publicacao = models.DateField(blank=True, null=True, help_text="Data de publicação no DOU")
    link_dou = models.URLField(blank=True, null=True, help_text="Link para a publicação no Diário Oficial da União")

    class Meta:
        verbose_name = "Lei Federal Previdenciária"
        verbose_name_plural = "Leis Federais Previdenciárias"

    def __str__(self):
        return f"Lei nº {self.numero}"

class DecretosModel(models.Model):
    """
    Modelo para armazenar informações sobre Decretos Federais.
    Ex: Decreto nº 8.424/2015, Decreto nº 12.527/2025
    """
    numero = models.CharField(max_length=50, unique=True, help_text="Número do Decreto (Ex: 8.424/2015)")
    ementa = models.TextField(blank=True, null=True, help_text="Ementa do Decreto")
    data_publicacao = models.DateField(blank=True, null=True, help_text="Data de publicação no DOU")
    link_dou = models.URLField(blank=True, null=True, help_text="Link para a publicação no Diário Oficial da União")

    class Meta:
        verbose_name = "Decreto Federal"
        verbose_name_plural = "Decretos Federais"

    def __str__(self):
        return f"Decreto nº {self.numero}"

class PortariasModel(models.Model):
    """
    Modelo para armazenar informações sobre Portarias (Federais, Estaduais, Municipais).
    Ex: Portarias do MPA, MMA, INSS, IEF-MG
    """
    numero = models.CharField(max_length=50, help_text="Número da Portaria (Ex: 154/2011)")
    ano = models.PositiveIntegerField(help_text="Ano da Portaria")
    orgao_emissor = models.CharField(max_length=100, help_text="Órgão que emitiu a Portaria (Ex: MPA, MMA, INSS, IEF-MG)")
    tipo = models.CharField(max_length=20, choices=TIPO_ATO_NORMATIVO_CHOICES, default='FEDERAL', help_text="Tipo de Portaria (Federal, Estadual, Municipal)")
    estado = models.CharField(max_length=20, choices=UF_CHOICES, blank=True, null=True, help_text="UF, se for uma Portaria Estadual")
    ementa = models.TextField(blank=True, null=True, help_text="Ementa da Portaria")
    data_publicacao = models.DateField(blank=True, null=True, help_text="Data de publicação")
    link_publicacao = models.URLField(blank=True, null=True, help_text="Link para a publicação oficial")

    class Meta:
        verbose_name = "Portaria"
        verbose_name_plural = "Portarias"
        unique_together = ('numero', 'ano', 'orgao_emissor', 'tipo', 'estado') # Para evitar duplicidade

    def __str__(self):
        return f"Portaria nº {self.numero}/{self.ano} - {self.orgao_emissor}"

class InstrucoesNormativasModel(models.Model):
    """
    Modelo para armazenar informações sobre Instruções Normativas.
    Ex: IN do INSS
    """
    numero = models.CharField(max_length=50, unique=True, help_text="Número da Instrução Normativa (Ex: 77/2015)")
    orgao_emissor = models.CharField(max_length=100, help_text="Órgão que emitiu a Instrução Normativa (Ex: INSS)")
    ementa = models.TextField(blank=True, null=True, help_text="Ementa da Instrução Normativa")
    data_publicacao = models.DateField(blank=True, null=True, help_text="Data de publicação")
    link_publicacao = models.URLField(blank=True, null=True, help_text="Link para a publicação oficial")

    class Meta:
        verbose_name = "Instrução Normativa"
        verbose_name_plural = "Instruções Normativas"

    def __str__(self):
        return f"IN nº {self.numero} - {self.orgao_emissor}"


class Especie(models.Model):
    """
    Modelo para armazenar informações sobre as espécies de pescado.
    """
    nome_cientifico = models.CharField(max_length=100, unique=True)
    nome_popular = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Espécie"
        verbose_name_plural = "Espécies"

    def __str__(self):
        return f"{self.nome_popular} ({self.nome_cientifico})"

class PeriodoDefesoOficial(models.Model):
    """
    Modelo para armazenar os períodos de defeso oficiais definidos por órgãos competentes.
    """
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE, help_text="Espécie alvo do defeso")
    orgao_definidor = models.CharField(max_length=100, help_text="Órgão que definiu o defeso (Ex: IBAMA, MPA/MMA)")
    ato_normativo_oficial = models.ForeignKey(
        PortariasModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='periodos_defeso',
        help_text="Portaria ou Decreto que estabeleceu este período de defeso"
    )
    data_inicio_oficial = models.DateField(help_text="Data de início oficial do defeso")
    data_fim_oficial = models.DateField(help_text="Data de fim oficial do defeso")
    estado = models.CharField(max_length=20, choices=UF_CHOICES, blank=True, null=True, help_text="UF, se o defeso for regionalizado")
    municipios_abrangidos = models.TextField(blank=True, null=True, help_text="Lista de municípios abrangidos, se aplicável")
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Período de Defeso Oficial"
        verbose_name_plural = "Períodos de Defeso Oficiais"
        unique_together = ('especie', 'data_inicio_oficial', 'data_fim_oficial', 'estado') # Para evitar duplicidade

    def __str__(self):
        return f"Defeso de {self.especie.nome_popular} em {self.estado or 'Nacional'} ({self.data_inicio_oficial} a {self.data_fim_oficial})"


class SeguroDefesoBeneficioModel(models.Model):
    """
    Modelo principal para gerenciar os benefícios do Seguro Defeso concedidos aos associados.
    """
    especie_alvo = models.ForeignKey(Especie, on_delete=models.SET_NULL, blank=True, null=True, help_text="Espécie para a qual o defeso foi concedido")
    
    # Referências aos atos normativos
    lei_federal = models.ForeignKey(
        LeiFederalPrevidenciaria,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='beneficios_defeso_lei',
        help_text="Lei Federal base para o benefício (Ex: Lei nº 10.779/2003)"
    )
    decreto_regulamentador = models.ForeignKey(
        DecretosModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='beneficios_defeso_decreto',
        help_text="Decreto que regulamenta a lei (Ex: Decreto nº 12.527/2025)"
    )
    instrucao_normativa = models.ForeignKey(
        InstrucoesNormativasModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='beneficios_defeso_in',
        help_text="Instrução Normativa aplicável (Ex: IN do INSS)"
    )
    portaria_especifica = models.ForeignKey(
        PortariasModel,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='beneficios_defeso_portaria',
        help_text="Portaria específica que define o período de defeso ou regras adicionais"
    )
    estado = models.CharField(max_length=20, choices=UF_CHOICES, help_text="Estado onde o associado reside e o defeso se aplica")
    # Período do benefício
    ano_concessao = models.PositiveIntegerField(default=date.today().year, help_text="Ano de concessão do benefício")
    data_inicio = models.DateField(help_text="Data de início do período de defeso para o benefício")
    data_fim = models.DateField(help_text="Data de fim do período de defeso para o benefício")
    
    class Meta:
        verbose_name = "Benefício Seguro Defeso"
        verbose_name_plural = "Benefícios Seguro Defeso"
        # Garante que um associado não tenha dois benefícios para a mesma espécie no mesmo período
        unique_together = ('especie_alvo', 'data_inicio', 'data_fim')

    def __str__(self):
        return f"Benefício para {self.especie_alvo} ({self.data_inicio} a {self.data_fim})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.aplicar_para_associados()

    def aplicar_para_associados(self):
        """
        Ao criar um Seguro Defeso, aplica para todos os associados ativos e que recebem seguro defeso.
        """
        associados = AssociadoModel.objects.filter(
            status__in=['associado_lista_ativo', 'associado_lista_aposentado'],  # ajuste se necessário
            recebe_seguro='Recebe',
            municipio_circunscricao__uf=self.estado
        )
        total_criados = 0
        for associado in associados:
            if not ControleBeneficioModel.objects.filter(associado=associado, beneficio=self).exists():
                ControleBeneficioModel.objects.create(
                    associado=associado,
                    beneficio=self,
                    status_pedido='EM_PREPARO',
                )
                total_criados += 1
        print(f"✅ {total_criados} controles criados para o benefício {self}")



def protocolo_upload_path(instance, filename):
    # Normaliza nome do associado
    nome_slug = slugify(instance.associado.user.get_full_name(), allow_unicode=True)
    ano = instance.beneficio.ano_concessao
    # Nome final do arquivo
    nome_arquivo = f"COMP_SEG_{nome_slug}_{ano}.pdf"
    # Retorna caminho relativo para o FileField
    return os.path.join('comprovantes_beneficio', nome_arquivo)    
        
        
class ControleBeneficioModel(models.Model):
    associado = models.ForeignKey('app_associados.AssociadoModel', on_delete=models.CASCADE, related_name='beneficios')
    beneficio = models.ForeignKey(SeguroDefesoBeneficioModel, on_delete=models.CASCADE, related_name='controles')
    numero_protocolo = models.CharField(max_length=50, blank=True, null=True)
    # Informações de localização e status
    status_pedido = models.CharField(max_length=40, choices=STATUS_BENEFICIO_CHOICES, default='EM_PREPARO', help_text="Status atual do benefício")
    data_solicitacao = models.DateField(blank=True, null=True, help_text="Data em que o benefício foi solicitado")
    data_concessao = models.DateField(blank=True, null=True, help_text="Data em que o benefício foi efetivamente concedido")
    motivo_exigencia = models.TextField(blank=True, null=True, help_text="Qual a Exigência é o que deve ser feito para cumprir")
    motivo_negativa = models.TextField(blank=True, null=True, help_text="Motivo se o benefício foi negado")
    anotacoes = models.TextField(blank=True, null=True, help_text="Anotações adicionais sobre o benefício")

    resultado_final = models.TextField(blank=True, null=True)
    comprovante_protocolo = models.FileField(
        upload_to=protocolo_upload_path,
        blank=True,
        null=True,
        verbose_name="Comprovante do Protocolo"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('associado', 'beneficio')
        ordering = ['-data_solicitacao']
        verbose_name = "Controle de Benefício"
        verbose_name_plural = "Controle de Benefícios"

    def __str__(self):
        return f"{self.associado} - {self.beneficio.lei_federal} ({self.status_pedido})"

