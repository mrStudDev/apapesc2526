# app_accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('superuser', 'Superusuário'),
        ('admin_associacao', 'Administrador Associação'),
        ('diretor', 'Diretor'),
        ('presidente', 'Presidente'),
        ('delagado', 'Delegado'),
        ('financeiro', 'Financeiro'),
        ('recursos_humanos', 'Recursos Humanos'),
        ('auxiliar_associacao', 'Auxilir Associação'),
        ('auxiliar_reparticao', 'Auxiliar Repartição'),
        ('auxiliar_extra', 'Auxiliar Extra'),
        ('cliente_vip', 'Cliente VIP'),
        ('cliente', 'Cliente'),
    )
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='cliente')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

