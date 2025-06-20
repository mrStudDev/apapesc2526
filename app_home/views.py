# Views/app_home/
# Imortações Padrões do Django - Base
from core.views.base_imports import *

#importação de Modelos - Formulários
from core.views.app_home_imports import *


class HomeListView(ListView):
    model = HomeModel
    template_name = 'home/home.html'
    context_object_name = 'ApapescHome'
