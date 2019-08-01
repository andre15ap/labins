from core.models import BasePadraoAbstract

from django.db import models



class Momento(BasePadraoAbstract):
    identificador = models.CharField('Identificador', max_length=100)
    inicio = models.DateField('Inicio do Momento')
    termino = models.DateField('Fim do Momento')

    class Meta:
        verbose_name = 'Momento'
        verbose_name_plural = 'Momentos'
        ordering = ['-ativo', '-data_alteracao' ]

    def __str__(self):
        return '{}.  {}/{}/{} - {}/{}/{}'.format(self.identificador, self.inicio.day, self.inicio.month,self.inicio.year, self.termino.day, self.termino.month, self.termino.year)

    def dependencia(self):
        from atividades.models import TurmaAtividade
        turmas_count = TurmaAtividade.objects.filter(momento__id=self.id, ativo=True).count()
        resultado = {}
        if turmas_count > 0:
            resultado['dependencia_turma'] = True
            turma_query = TurmaAtividade.objects.filter(momento__id=self.id, ativo=True)
            turma_list = []
            
            for turma in turma_query:
                campo = {}
                campo['turma'] = str(turma.nome)
                campo['id'] = str(turma.id)
                turma_list.append(campo)
                
            resultado['turma_list'] = turma_list
            
        else:
            resultado['dependencia_turma'] = False
            
        return resultado

class Campus(BasePadraoAbstract):
    nome = models.CharField('Nome do Campus', max_length=100)
    descricao = models.TextField('Informação Extra', blank=True, null=True)

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campus'
        ordering = ['-ativo', 'nome' ]

    def __str__(self):
        return self.nome

    def dependencia(self):
        #VERIFICAR SE EXISTE PREDIOS OU CURSOS/SETORES ATIVOS QUE PERTENCAM AO CAMPUS
        predios_count = Predio.objects.filter(campus__id=self.id, ativo=True).count() 
        curos_setores_count = CursoSetor.objects.filter(campus__id=self.id, ativo=True).count() 
		
        resultado = {}

	    #EXISTE PREDIO ATIVO, NAO PODE SER DESATIVADO
        if predios_count > 0:
            resultado['dependencia_predio'] = True
            predio_query = Predio.objects.filter(campus__id=self.id, ativo=True)
            predio_list = []

            for predio in predio_query:
                linha = {}
                linha['predio'] = str(predio.identificador)
                linha['id'] = str(predio.id)
                predio_list.append(linha)

                resultado['predio_list'] = predio_list
        else:
            resultado['dependencia_predio'] = False

        #EXISTE CURSO/SETOR ATIVO, NAO PODE SER DESATIVADO
        if curos_setores_count > 0:
            resultado['dependencia_curso_setor'] = True
            curso_setor_query = CursoSetor.objects.filter(campus__id=self.id, ativo=True)
            curso_setor_list = []

            for curso_setor in curso_setor_query:
                linha = {}
                linha['curso_setor'] = str(curso_setor.nome)
                linha['id'] = str(curso_setor.id)
                curso_setor_list.append(linha)

                resultado['curso_setor_list'] = curso_setor_list
        else:
            resultado['dependencia_curso_setor'] = False

        return resultado


class CursoSetor(BasePadraoAbstract):
    CURSO = 'Curso'
    SETOR = 'Setor'

    CHOICES_CURSO_SETOR = (
        (CURSO, 'Curso'),
        (SETOR, 'Setor'),
    )

    nome = models.CharField('Nome Curso', max_length=255)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    tipo = models.CharField('Curso ou Setor?', max_length=25, choices=CHOICES_CURSO_SETOR)

    class Meta:
        verbose_name = "Curso / Setor"
        verbose_name_plural = "Cursos e Setores"
        ordering = ['-ativo', 'nome']

    def __str__(self):
        return self.nome +' - '+self.tipo

    def dependencia(self):
        #VERIFICAR SE EXISTE SOLICITANTE ATIVOS QUE PERTENCAM AO TIPO-SOLICINTATE
        from contas.models import Solicitante
        from atividades.models import Atividade
        solicitante_count = Solicitante.objects.filter(curso_setor__id=self.id, ativo=True).count()  
        atividade_count = Atividade.objects.filter(curso_setor__id=self.id, ativo=True).count()
        resultado = {}

	    #EXISTE SOLICITANTE ATIVO, NAO PODE SER DESATIVADO
        if solicitante_count > 0:
            resultado['dependencia_solicitante'] = True
            solicitante_query = Solicitante.objects.filter(curso_setor__id=self.id, ativo=True)
            solicitante_list = []

            for solicitante in solicitante_query:
                linha = {}
                linha['solicitante'] = str(solicitante)
                linha['id'] = str(solicitante.id)
                solicitante_list.append(linha)

                resultado['solicitante_list'] = solicitante_list
        else:
            resultado['dependencia_solicitante'] = False
        
        #EXISTE ATIVIDADE ATIVO, NAO PODE SER DESATIVADO
        if atividade_count > 0:
            resultado['dependencia_atividade'] = True
            atividade_query = Atividade.objects.filter(curso_setor=self.id, ativo=True)
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


class Predio(BasePadraoAbstract):
    identificador = models.CharField('Indentificador do Prédio', max_length=100)
    descricao = models.TextField('Informação extra',help_text='alguma observação sobre o prédio')
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Prédio'
        verbose_name_plural = 'Prédios'
        ordering = ['-ativo', 'identificador' ]

    def __str__(self):
        return self.identificador

    def dependencia(self):
        #VERIFICAR SE EXISTE PREDIOS OU CURSOS/SETORES ATIVOS QUE PERTENCAM AO CAMPUS
        sala_count = Sala.objects.filter(predio__id=self.id, ativo=True).count()  
        resultado = {}

	    #EXISTE SALA ATIVO, NAO PODE SER DESATIVADO
        if sala_count > 0:
            resultado['dependencia_sala'] = True
            sala_query = Sala.objects.filter(predio__id=self.id, ativo=True)
            sala_list = []

            for sala in sala_query:
                linha = {}
                linha['sala'] = str(sala.identificador)
                linha['id'] = str(sala.id)
                sala_list.append(linha)

                resultado['sala_list'] = sala_list
        else:
            resultado['dependencia_sala'] = False

        return resultado


class FotoPredio(BasePadraoAbstract):
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, blank=True, null=True)
    foto = models.ImageField(upload_to='predios',blank=False, null=True)

    class Meta:
        verbose_name = 'Foto do Prédio'
        verbose_name_plural = 'Fotos do Prédio'

    # def __str__(self):
    #     return 'Prédio: {}'.format(self.nome)

class DescrisaoEspaco(BasePadraoAbstract):
    descricao = models.TextField('Informação sobre o espaço')
    qtd_tomadas = models.PositiveIntegerField('Quantidade de tomadas')
    qtd_computadores = models.PositiveIntegerField('Quantidade de computadores')

    class Meta:
        verbose_name = 'Descrição da sala'
        verbose_name_plural = 'Descrições das salas'

    def __str__(self):
        return 'Descrição: {}'.format(self.descricao)

class Sala(BasePadraoAbstract):
    identificador = models.CharField('Número/Idenfificador da sala', max_length=100, blank=False, null=False)
    predio = models.ForeignKey(Predio, blank=False, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-ativo','identificador']

    def __str__(self):
        return 'Sala {} - {}'.format(self.identificador,self.predio)

    def dependencia(self):
        #VERIFICAR SE EXISTEM ESPACOS ATIVOS QUE PERTENCAM A SALA
        espaco_count = Espaco.objects.filter(sala__id=self.id, ativo=True).count()  
        resultado = {}

	    #EXISTE ESPACO ATIVO, NAO PODE SER DESATIVADO
        if espaco_count > 0:
            resultado['dependencia_espaco'] = True
            espaco_query = Espaco.objects.filter(sala__id=self.id, ativo=True)
            espaco_list = []

            for espaco in espaco_query:
                linha = {}
                linha['espaco'] = str(espaco.identificador)
                linha['id'] = str(espaco.id)
                espaco_list.append(linha)

                resultado['espaco_list'] = espaco_list
        else:
            resultado['dependencia_espaco'] = False

        return resultado

class Espaco(BasePadraoAbstract):
    identificador = models.CharField('Indentificador do Espaço', max_length=100)
    descricao = models.TextField('Informação extra', blank=True, null=True)
    sala = models.ForeignKey(Sala, blank=False, null=True, on_delete=models.SET_NULL)
    qtd_bancadas = models.PositiveIntegerField('Quantidade de bancadas livres', default=0)
    qtd_computadores = models.PositiveIntegerField('Quantidade de computadores', default=0)
    

    class Meta:
        verbose_name = 'Espaço'
        verbose_name_plural = 'Espaços'
        ordering = ['-ativo','identificador']

    def __str__(self):
        return self.identificador


class FotoEspaco(BasePadraoAbstract):
    espaco = models.ForeignKey(Espaco, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='salas')

    class Meta:
        verbose_name = 'Foto do Espaço'
        verbose_name_plural = 'Fotos do Espaço'
