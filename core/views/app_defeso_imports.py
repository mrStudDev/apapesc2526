from  app_defeso.models import (
    SeguroDefesoBeneficioModel,
    ControleBeneficioModel,
    ProcessamentoSeguroDefesoModel,
    pegar_proximo_defeso_para_usuario,
    resetar_processamento_rodada,
    finalizar_processamento_defeso,
    )
from app_defeso.forms import ControleBeneficioForm
from app_uploads.models import UploadsDocs
from core.choices import STATUS_BENEFICIO_CHOICES