
from contas.models import Solicitante, SuporteConta, TipoSolicitante, Usuario
from academico.models import Campus, CursoSetor, Momento, Predio, Sala, Espaco
from atividades.models import SistemaOperacional, Software, TipoAtividade, Atividade, TurmaAtividade, Reserva


class Criar:
    def __init__(self):
        print('-------criando objetos -----------')
        self.executar()

    def executar(self):
        try:
            #SUPER USER
            super_user_count = Usuario.objects.filter(is_superuser=True).count()
            if super_user_count == 0:
                user=Usuario.objects.create_user('00000000000', password='asdfghjkl')
                user.is_superuser=True
                user.is_staff=True
                user.save()

            
            #SUPORTE DE CONTAS, ESTAGIARIOS
            estagiario_1 = SuporteConta.objects.create_user('11111111111', password='senha1234')
            estagiario_1.first_name='Adriel'
            estagiario_1.last_name='Pereira'
            estagiario_1.telefone='92334455'
            estagiario_1.email='adriel@gmail.com'
            estagiario_1.save()

            estagiario_2 = SuporteConta.objects.create_user('22222222222', password='senha1234')
            estagiario_2.first_name='Jonatan'
            estagiario_2.last_name='da Silva'
            estagiario_2.telefone='84112233'
            estagiario_2.email='jonatan@gmail.com'
            estagiario_2.save()

            # CAMPUS
            palmas = Campus(nome='Palmas', descricao='Campus universitário de Palmas')
            palmas.save()
            araguarina = Campus(nome='Araguaina', descricao='Campus universitário de Araguaina')
            araguarina.save()

            #CURSOS E SETORES
            computacao = CursoSetor(nome='Ciência da Computação', campus=palmas, tipo='Curso')
            computacao.save()
            engenharia_ambiental = CursoSetor(nome='Engenharia Ambiental', campus=palmas, tipo='Curso')
            engenharia_ambiental.save()

            #TIPOS DE SOLICITANTES
            aluno = TipoSolicitante(tipo='Aluno', descricao='Aluno da Uft')
            aluno.save()
            professor = TipoSolicitante(tipo='Professor', descricao='Professor da Uft')
            professor.save()

            # SOCICITANTES
            solicitante_1 = Solicitante.objects.create_user('33333333333', password='senha1234')
            solicitante_1.first_name='Pedro'
            solicitante_1.last_name='Gonzada Cardoso'
            solicitante_1.curso_setor=computacao
            solicitante_1.tipo_solicitante=aluno
            solicitante_1.telefone='99998888'
            solicitante_1.email='pedro@gmail.com'
            solicitante_1.save()

            solicitante_2 = Solicitante.objects.create_user('44444444444', password='senha1234')
            solicitante_2.first_name='Maria'
            solicitante_2.last_name='Joaquina Francisca'
            solicitante_2.curso_setor=engenharia_ambiental
            solicitante_2.tipo_solicitante=professor
            solicitante_2.telefone='99998888'
            solicitante_2.email='maria@gmail.com'
            solicitante_2.save()

            #MOMENTOS
            momento = Momento(identificador='2018-2', inicio='2018-08-01', termino='2018-11-30', ativo=True)
            momento.save()

            #PREDIOS 
            bloco_2 = Predio(identificador='Bloco 2', descricao='Bloco Fisico da uft', campus=palmas)
            bloco_2.save()
            bloco_3 = Predio(identificador='Bloco 3', descricao='Bloco Fisico da uft', campus=palmas)
            bloco_3.save()

            #SALAS
            sala_1 = Sala(identificador='12', predio=bloco_3)
            sala_1.save()
            sala_2 = Sala(identificador='15', predio=bloco_3)
            sala_2.save()

            #ESPAÇOS
            espaco_1 = Espaco(identificador='labin 12',descricao='laboratório com computadores de uso comum', sala=sala_1, qtd_bancadas=5, qtd_computadores=20)
            espaco_1.save() 
            espaco_2 = Espaco(identificador='labin 15',descricao='laboratório com computadores de uso comum', sala=sala_2, qtd_bancadas=5, qtd_computadores=20)
            espaco_2.save()

            #SISTEMAS OPERACIONAIS
            windows = SistemaOperacional(nome='Windows 10', versao='Ultimate Estável')
            windows.save()
            ubuntu = SistemaOperacional(nome='Ubuntu 18', versao='LTS')
            ubuntu.save()
            
            #SOFTWARES
            excel = Software(nome='Office 2018', sistema=windows, descricao='do pacote microsoft office')
            excel.save()
            sublime = Software(nome='Sublime Text', sistema=ubuntu, descricao='Editor de texto para programar')
            sublime.save()

            #TIPOS DE ATIVIDADES
            aula = TipoAtividade(identificador= 'Aula', descricao='tipo de atividade exercida por professor')
            aula.save()
            curso = TipoAtividade(identificador='Curso', descricao='tipo de atividade temporario')
            curso.save()

            #ATIVIDADES
            comp_grafica = Atividade(nome='Computação Grafica', descricao='Aula de computação grafica de computação', tipo_atividade=aula, curso_setor=computacao, solicitante=solicitante_2, ativo=False)
            comp_grafica.save()
            curso_prog = Atividade(nome='Curso Programação', descricao='Curso de programação basica para engenharia', tipo_atividade=curso, curso_setor=engenharia_ambiental, solicitante=solicitante_1, ativo=True)
            curso_prog.save()
                
            print('------------ criou --------------')
        except:
            print(' -_-  algo de errado não esta certo -_- ')




    def solicitates(self):
        pass



