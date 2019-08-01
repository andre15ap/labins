
from django import template

from contas.models import SuporteConta, Solicitante, Administrador
from atividades.models import TurmaAtividade

register = template.Library()



@register.filter(name='permissao_suporte')
def permissao_suporte(user):
    try:
        usuario = SuporteConta.objects.get(id=user.id)
        return True
    except:
        pass
    return False


@register.filter(name='tipo_usuario')
def tipo_usuario(user, tipo):
    if tipo == 'solicitante':
        try:
            usuario = Solicitante.objects.get(id=user.id)
            return True
        except:
            pass
    elif tipo == 'suporte':
        try:
            usuario = SuporteConta.objects.get(id=user.id)
            return True
        except:
            pass
    
    elif tipo == 'administrador':
        try:
            usuario = Administrador.objects.get(id=user.id)
            return True
        except:
            pass
    
    return False