from django.db.models.signals import post_save
from django.dispatch import receiver
from models import ServicoModel, EntradaFinanceiraModel


@receiver(post_save, sender=ServicoModel)
def criar_entrada_financeira_automaticamente(sender, instance, created, **kwargs):
    if created and instance.precisa_entrada_financeira():
        # Só cria se não existir ainda
        if not hasattr(instance, 'entrada_servico'):
            EntradaFinanceiraModel.objects.create(
                servico=instance,
                valor=instance.valor,
                forma_pagamento='dinheiro', 
                parcelamento='avista',     
            )
