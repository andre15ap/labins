# from django.contrib.auth.models import User
# site para class base view ccbv.co.uk
# sobrescrever com baseUser user
# User = get_user_model()
# from django.contrib.auth import get_user_model

from core.models import BasePadraoAbstract
from django.db import models
from django.contrib.auth.models import AbstractUser


from academico.models import CursoSetor


class Usuario(AbstractUser, BasePadraoAbstract):
    telefone = models.CharField('Telefone', max_length=25)
    foto = models.ImageField(upload_to='imagens', blank=False, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    def permissao_suporte(self):
        try:
            usuario = SuporteConta.objects.get(id=self.id)
            return True
        except:
            pass
        return False
    def permissao_solicitante(self):
        try:
            usuario = Solicitante.objects.get(id=self.id)
            return True
        except:
            pass
        return False

    def dependencia(self):
        #VERIFICAR SE EXISTE ATIVIDADE ATIVOS QUE PERTENCAM AO SOLICITANTE
        from atividades.models import Atividade
        atividade_count = Atividade.objects.filter(solicitante__id=self.id, ativo=True).count()  
        resultado = {}

	    #EXISTE ATIVIDADE ATIVO, NAO PODE SER DESATIVADO
        if atividade_count > 0:
            resultado['dependencia_atividade'] = True
            atividade_query = Atividade.objects.filter(solicitante__id=self.id, ativo=True)
            atividade_list = []

            for atividade in atividade_query:
                linha = {}
                linha['atividade'] = str(atividade)
                linha['id'] = str(atividade.id)
                atividade_list.append(linha)

                resultado['atividade_list'] = atividade_list
        else:
            resultado['dependencia_atividade'] = False

        return resultado


#ex professor, aluno ou tecnico
class TipoSolicitante(BasePadraoAbstract):
    tipo = models.CharField('Tipo Solicitante', max_length=100)
    descricao = models.TextField('Descrição do Tipo Solicitante', null=True, blank=True)

    class Meta:
        verbose_name = 'Tipo Solicitante'
        verbose_name_plural = 'Tipos Solicitante'
        ordering = ['-ativo', 'tipo']
        

    def __str__(self):
        return self.tipo

    def dependencia(self):
        #VERIFICAR SE EXISTE SOLICITANTE ATIVOS QUE PERTENCAM AO TIPO-SOLICINTATE
        solicitante_count = Solicitante.objects.filter(tipo_solicitante__id=self.id, ativo=True).count()  
        resultado = {}

	    #EXISTE SOLICITANTE ATIVO, NAO PODE SER DESATIVADO
        if solicitante_count > 0:
            resultado['dependencia_solicitante'] = True
            solicitante_query = Solicitante.objects.filter(tipo_solicitante__id=self.id, ativo=True)
            solicitante_list = []

            for solicitante in solicitante_query:
                linha = {}
                linha['solicitante'] = str(solicitante)
                linha['id'] = str(solicitante.id)
                solicitante_list.append(linha)

                resultado['solicitante_list'] = solicitante_list
        else:
            resultado['dependencia_solicitante'] = False

        return resultado


class Horario(BasePadraoAbstract):
    SEGUNDA = 'Segunda'
    TERCA = 'Terça'
    QUARTA = 'Quarta'
    QUINTA = 'Quinta'
    SEXTA = 'Sexta'
    SABADO = 'Sabado'
    DOMINGO = 'Domingo'

    CHOICES_DIA_SEMANA = (
        (DOMINGO, 'Domingo'),
        (SEGUNDA, 'Segunda'),
        (TERCA, 'Terça'),
        (QUARTA, 'Quarta'),
        (QUINTA, 'Quinta'),
        (SEXTA, 'Sexta'),
        (SABADO, 'Sabado'),
    )
    dia_semana = models.CharField('Dia da Semana', max_length=15, choices=CHOICES_DIA_SEMANA, default=SEGUNDA)
    horario_inicio = models.TimeField('Horário de inicio do Estagio')
    horario_fim = models.TimeField('Horário de Fim do Estagio')

class SuporteConta(Usuario):
    horarios = models.ManyToManyField(Horario, blank=True)
    
    class Meta:
        verbose_name = 'suporte de Contas'
        verbose_name_plural = 'suportes de Contas'



# classe do solicitante
class Solicitante(Usuario):
    tipo_solicitante = models.ForeignKey(TipoSolicitante,null=True, blank=False, on_delete=models.CASCADE)
    curso_setor = models.ForeignKey(CursoSetor, null=True, blank=False, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Solicitante'
        verbose_name_plural = 'Solicitantes'
        ordering = ['-ativo', 'first_name']


    # def liberar(self, user):
    #     responsavel_count = SuporteConta.objects.filter(id=user.id).count()
    #     if responsavel_count == 1:
    #         self.is_active = True
    #         self.liberado = 
    #         self.save()
    #         return True
    #     return False
    # def ativa_desativa(self, user):
    #     #NÃO TEM RESPONSAVEL, O USER VAI SER O RESPONSAVEL
    #     responsavel_count = SuporteConta.objects.filter(id=user.id).count()
    #     if responsavel_count == 1:
    #         self.is_active = not self.is_active
    #         self.save()
    #         return True
    #     return False


class Administrador(Usuario):
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'



class HorarioSuporte(BasePadraoAbstract):
    suporte = models.ForeignKey(SuporteConta, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Horário de Suporte'
        verbose_name_plural = 'Horários de Suporte'

    def __str__(self):
        return '{}. De: {}, Até {}'.format(self.suporte, self.horario.horario_inicio, self.horario.horario_fim)  




# class BatePapo(BasePadraoAbstract):
#     criador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='bate_papo_criador')

#     class Meta:
#         verbose_name = 'Bate Papo'
#         verbose_name_plural = 'Bate Papos'
#         ordering = ['criador']

#     def __str__(self):
#         return 'Criador: {}'.format(self.criador)

# #criar campo para saber se mensagem foi finalizada
# #talvez agrupar mensagens
# class Mensagem(models.Model):
#     bate_papo = models.ForeignKey(BatePapo, on_delete=models.CASCADE, related_name='msg_bate_papo')
#     mensagem = models.TextField('Mensagem')
#     remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='msg_remetente')
#     destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='msg_destinatario')
#     data = models.DateTimeField('Data Mensagem', auto_now_add=True)

#     class Meta:
#         verbose_name = 'Mensagem'
#         verbose_name_plural = 'Mensagens'
#         ordering = ['data']

#     def __str__(self):
#         return 'De: {}. Para: {} '.format(self.remetente, self.destinatario)



