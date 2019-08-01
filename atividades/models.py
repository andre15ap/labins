from core.models import BasePadraoAbstract

from datetime import date

from django.db import models

from contas.models import Solicitante, SuporteConta
from academico.models import Momento, CursoSetor, Campus, Espaco



#usuairo solocita o cadastro de 'software' e sistema operacional
class SistemaOperacional(BasePadraoAbstract):
    nome = models.CharField('Nome do Sistema Operacional', max_length=255)
    versao = models.CharField('Versão do Sistema', max_length=100)

    class Meta:
        verbose_name = 'Sistema Operacional'
        verbose_name_plural = 'Sistemas Operacionais'
        ordering = ['-ativo', 'nome']

    def __str__(self):
        return self.nome

    def dependencia(self):
        #VERIFICAR SE EXISTE SOFTWARES ATIVOS QUE PERTENCAM AO TIPO SO
        software_count = Software.objects.filter(sistema__id=self.id, ativo=True).count()
        resultado = {}

	    #EXISTE SOFTWARE ATIVO, NAO PODE SER DESATIVADO
        if software_count > 0:
            resultado['dependencia_software'] = True
            software_query = Software.objects.filter(sistema__id=self.id, ativo=True)
            software_list = []

            for software in software_query:
                linha = {}
                linha['software'] = str(software.nome)
                linha['id'] = str(software.id)
                software_list.append(linha)

                resultado['software_list'] = software_list
        else:
            resultado['dependencia_software'] = False

        return resultado


class Software(BasePadraoAbstract):
    nome = models.CharField('Nome do Programa', max_length=255)
    sistema = models.ForeignKey(SistemaOperacional,on_delete=models.CASCADE, related_name="atividade_solicitante")
    descricao = models.TextField('Descrição do Programa')

    class Meta:
        verbose_name = 'Software'
        verbose_name_plural = 'softwares'
        ordering = ['-ativo', 'nome']

    def __str__(self):
        return '{} | SO: {}'.format(self.nome, self.sistema.nome)

    def dependencia(self):
        #VERIFICAR SE EXISTE TURMAS ATIVAS QUE TENHA AO TIPO SOFTWARE
        turma_query = TurmaAtividade.objects.filter(ativo=True)
        software = Software.objects.get(id=self.id)
        turma_list = []
        resultado = {}
        resultado['dependencia_turma'] = False
        for turma in turma_query:
            if software in turma.softwares.all():
                resultado['dependencia_turma'] = True
                linha = {}
                linha['turma'] = str(turma.nome)
                linha['id'] = str(turma.id)
                turma_list.append(linha)

        resultado['turma_list'] = turma_list
        return resultado

class FotoAviso(BasePadraoAbstract):
    foto = models.ImageField(upload_to='avisos',blank=False, null=True)
    responsavel = models.ForeignKey(SuporteConta, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Foto de aviso'
        verbose_name_plural = 'Fotos de Avisos'

# o tipo de atividade vai conter a quantidade total de encontros
class TipoAtividade(BasePadraoAbstract):
    identificador = models.CharField('Tipo da Atividade', max_length=50)
    descricao =  models.TextField('Descrição do Tipo de Atividade', blank=True, null=True)
    # qtd_encontro = models.PositiveIntegerField('Quantidade de Encontros')

    class Meta:
        verbose_name = 'Tipo de Atividade'
        verbose_name_plural = 'Tipos de Atividades'
        ordering = ['-ativo', 'identificador']

    def __str__(self):
        return self.identificador

    def dependencia(self):
        #VERIFICAR SE EXISTE ATIVIDADES ATIVOS QUE PERTENCAM AO TIPO ATIVIDADE
        atividade_count = Atividade.objects.filter(tipo_atividade__id=self.id, ativo=True).count()
        resultado = {}

	    #EXISTE ATIVIDADE ATIVO, NAO PODE SER DESATIVADO
        if atividade_count > 0:
            resultado['dependencia_atividade'] = True
            atividade_query = Atividade.objects.filter(tipo_atividade__id=self.id, ativo=True)
            atividade_list = []

            for atividade in atividade_query:
                linha = {}
                linha['atividade'] = str(atividade.nome)
                linha['id'] = str(atividade.id)
                atividade_list.append(linha)

                resultado['atividade_list'] = atividade_list
        else:
            resultado['dependencia_atividade'] = False

        return resultado

#duvida, qual status colocar quando criada a atividade? se nao for statico os status
class Atividade(BasePadraoAbstract):
    nome = models.CharField('Nome Atividade/Disciplina', max_length=125)
    descricao = models.TextField('Descrição da Atividade/Disciplina')
    tipo_atividade = models.ForeignKey(TipoAtividade, null=True, on_delete=models.SET_NULL)
    curso_setor =  models.ForeignKey(CursoSetor, null=True, on_delete=models.SET_NULL)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    liberada = models.BooleanField('Foi liberada?', blank=True, default=False)

    class Meta:
        ordering = ['-ativo', 'nome', '-data_alteracao' ]

    def __str__(self):
        return self.nome




class TurmaAtividade(BasePadraoAbstract):
    #FOI ATIVA, E O SUPORTE DEIXOU DE SER O RESPONSAVEL
    AGUARDANDO = 'Aguardando'
    #ESTA ATIVA E PODE FAZER RESERVA
    ATIVA = 'Ativa'
    #FOI EDITADA, NECESSITA DE AUTORIZACAO
    BLOQUEADA = 'Bloqueada'
    #NOVA, NECESSITA DE AUTORIZAÇAO
    CRIADA = 'Cridada'
    #FECHADA, O SUPORTE PRECISA ENCERRAR PARA PODER CRIAR NOVAS TURMAS
    ENCERRADA = 'Encerrada'

    CHOICES_STATUS_TURMA = (
        (AGUARDANDO, 'Aguardando'),
        (ATIVA, 'Ativa'),
        (BLOQUEADA, 'Bloqueada'),
        (CRIADA, 'Criada'),
        (ENCERRADA, 'Encerrada'),
    )
    nome = models.CharField('Nome da Turma', max_length=125)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, blank=True, null=True)
    responsavel = models.ForeignKey(SuporteConta, null=True, blank=True, on_delete=models.SET_NULL, related_name='suporte_responsavel')
    momento = models.ForeignKey(Momento, blank=True, null=True, on_delete=models.SET_NULL)
    qtd_computadores = models.PositiveIntegerField('Quantidade de computadore', default=0)
    qtd_bancadas = models.PositiveIntegerField('Quantidade de bancadas livres', default=0)
    softwares = models.ManyToManyField(Software, blank=True,help_text='mantenha a tecla CTRL precionada e escolha os softwares')
    status = models.CharField('Status', max_length=25, choices=CHOICES_STATUS_TURMA)
    espacos_liberados = models.ManyToManyField(Espaco, blank=True)
    qtd_encontro = models.PositiveIntegerField('Quantidade de encontros',default=19, blank=True)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['status', 'nome']

    def __str__(self):
        if not self.status == self.CRIADA:
            return 'Turma: {} - {} - {}'.format(self.nome,self.atividade.solicitante.first_name, self.atividade.solicitante.email)
        else:
            return 'Nova Turma: {}'.format(self.nome)

    @staticmethod
    def desativar_auto():
        hoje = date.today()
        for turma in TurmaAtividade.objects.filter(ativo=True):
            try:
                if turma.momento.termino < hoje:
                    turma.ativo = False
                    print('desativou turma {}'.format(turma))
                    turma.status = turma.ENCERRADA
                    turma.save()
            except:
                pass

    def verifica_criar_turma(self, atividade):
        turmas_count = TurmaAtividade.objects.filter(atividade=atividade).count()

        if turmas_count == 0:
            return True
        else:
            turmas_nao_encerradas_count = TurmaAtividade.objects.filter(atividade=atividade).exclude(status='encerrada').count()
            if turmas_nao_encerradas_count > 0:
                return False
        return True

    def autualiza_responsavel(self, user):
        suporte_count = SuporteConta.objects.filter(id=user.id).count()
        resultado = {}
        resultado['permitido_atualizar'] = False
        if suporte_count == 1:
            suporteConta = SuporteConta.objects.get(id=user.id)
            resultado['permitido_atualizar'] = True
            #NÃO TEM RESPONSAVEL, O USER VAI SER O RESPONSAVEL
            if not self.responsavel:
                self.responsavel = suporteConta
                self.status = self.ATIVA
                self.save()
                resultado['responsavel'] = str(suporteConta)
                resultado['status'] = str(self.ATIVA)
            #JA TEM RESPONSAVEL, VERIFICAR SE USER É O RESPONSAVEL PARA DEIXAR
            else:
                if suporteConta == self.responsavel:
                    self.responsavel = None
                    self.status = self.AGUARDANDO
                    self.save()
                    resultado['responsavel'] = 'Sem Responsável'
                    resultado['status'] = str(self.AGUARDANDO)
        return resultado

    def dependencia(self):
        #VERIFICAR SE EXISTE Reservas ATIVOS QUE PERTENCAM A turma
        reserva_count = Reserva.objects.filter(turma__id=self.id, ativo=True).count()
        resultado = {}

	    #EXISTE SOFTWARE ATIVO, NAO PODE SER DESATIVADO
        if reserva_count > 0:
            resultado['dependencia_reserva'] = True
        else:
            resultado['dependencia_reserva'] = False

        return resultado


class Reserva(BasePadraoAbstract):
    MANHA = 'Manha'
    TARDE = 'Tarde'
    NOITE = 'Noite'

    CHOICES_TURNO = (
        (MANHA, 'Manha'),
        (TARDE, 'Tarde'),
        (NOITE, 'Noite'),
    )

    espaco = models.ForeignKey(Espaco,null=True, blank=True, on_delete=models.SET_NULL)
    dia = models.DateField('Dia Reserva')
    turno = models.CharField('Turno', max_length=12, choices=CHOICES_TURNO)
    turma = models.ForeignKey(TurmaAtividade, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        unique_together = ("espaco", "dia", "turno")
        ordering = ['dia']

    def __str__(self):
        return 'Dia {}/{}/{}, Turno: {}'.format(str(self.dia.day),str(self.dia.month),str(self.dia.year), self.turno)

    @staticmethod
    def desativar_auto():
        hoje = date.today()
        for reserva in Reserva.objects.filter(ativo=True):
            if reserva.dia < hoje:
                reserva.ativo = False
                print('desativou reserva {}'.format(reserva.dia))
                reserva.save()


    def criar(self):
        existem_count = Reserva.objects.filter(dia=self.dia,turno=self.turno, espaco=self.espaco).count()
        if existem_count > 0:
            return False
        self.save()
        return True

    def retorna_dias(self, momento):
        lista = []
        atual = momento.inicio
        while atual <= momento.final:
            print(atual)
