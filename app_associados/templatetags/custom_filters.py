from django import template

register = template.Library()

@register.filter
def is_in(value, arg):
    """Verifica se value está em arg (string separada por espaço ou lista)."""
    return value in arg.split() if isinstance(arg, str) else value in arg
