from django import template

from contas.models import SuporteConta
from atividades.models import TurmaAtividade, Reserva

register = template.Library()


@register.filter(name='qtd_turmas')
def qtd_turmas(user):
    # print('---------- entrou ')
    turmas_count = TurmaAtividade.objects.filter(responsavel__id=user.id, status='Ativa').count()
    return turmas_count

@register.filter(name='turma_ativa')
def turma_ativa(turma):
    if turma.status == turma.ATIVA:
        return True
    return False

@register.filter(name='turma_js')
def turma_js(obj):
    return mark_safe(json.dumps(obj))

@register.filter(name='dia_semana')
def dia_semana(dia):
    DIAS = [
        'Segunda-Feira',
        'Terça-Feira',
        'Quarta-Feira',
        'Quinta-Feira',
        'Sexta-Feira',
        'Sabado',
        'Domingo'
    ]

    indice = dia.weekday()
    dia_escrito = DIAS[indice]

    return dia_escrito


@register.filter(name='reserva_dia')
def reserva_dia(dia, espaco):
    if not dia['Manha']:
        turno = 'Manha'
    elif not dia['Tarde']:
        turno = 'Tarde'
    elif not dia['Noite']:
        turno = 'Noite'
    # print('{} {} {}'.format(dia['dia'], turno, espaco))
    try:
        reserva = Reserva.objects.get(dia=dia['dia'], espaco=espaco, turno=turno)
        turma = reserva.turma
    except:
        turma = None
    
    return turma