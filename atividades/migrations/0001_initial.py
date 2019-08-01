# Generated by Django 2.1.1 on 2018-12-20 18:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academico', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão da foto')),
                ('data_alteracao', models.DateField(auto_now=True, verbose_name='Data de inclusão da foto')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=125, verbose_name='Nome Atividade/Disciplina')),
                ('descricao', models.TextField(verbose_name='Descrição da Atividade/Disciplina')),
                ('liberada', models.BooleanField(blank=True, default=False, verbose_name='Foi liberada?')),
            ],
            options={
                'ordering': ['-ativo', 'nome', '-data_alteracao'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão da foto')),
                ('data_alteracao', models.DateField(auto_now=True, verbose_name='Data de inclusão da foto')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo?')),
                ('dia', models.DateField(verbose_name='Dia Reserva')),
                ('turno', models.CharField(choices=[('Manha', 'Manha'), ('Tarde', 'Tarde'), ('Noite', 'Noite')], max_length=12, verbose_name='Turno')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['dia'],
            },
        ),
        migrations.CreateModel(
            name='SistemaOperacional',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão da foto')),
                ('data_alteracao', models.DateField(auto_now=True, verbose_name='Data de inclusão da foto')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome do Sistema Operacional')),
                ('versao', models.CharField(max_length=100, verbose_name='Versão do Sistema')),
            ],
            options={
                'verbose_name': 'Sistema Operacional',
                'verbose_name_plural': 'Sistemas Operacionais',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão da foto')),
                ('data_alteracao', models.DateField(auto_now=True, verbose_name='Data de inclusão da foto')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome do Programa')),
                ('descricao', models.TextField(verbose_name='Descrição do Programa')),
            ],
            options={
                'verbose_name': 'Software',
                'verbose_name_plural': 'softwares',
            },
        ),
        migrations.CreateModel(
            name='TipoAtividade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão da foto')),
                ('data_alteracao', models.DateField(auto_now=True, verbose_name='Data de inclusão da foto')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo?')),
                ('identificador', models.CharField(max_length=50, verbose_name='Tipo da Atividade')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição do Tipo de Atividade')),
            ],
            options={
                'verbose_name': 'Tipo de Atividade',
                'verbose_name_plural': 'Tipos de Atividades',
            },
        ),
        migrations.CreateModel(
            name='TurmaAtividade',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão da foto')),
                ('data_alteracao', models.DateField(auto_now=True, verbose_name='Data de inclusão da foto')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo?')),
                ('nome', models.CharField(max_length=125, verbose_name='Nome da Turma')),
                ('qtd_computadores', models.PositiveIntegerField(default=0, verbose_name='Quantidade de computadore')),
                ('qtd_bancadas', models.PositiveIntegerField(default=0, verbose_name='Quantidade de bancadas livres')),
                ('status', models.CharField(choices=[('Aguardando', 'Aguardando'), ('Ativa', 'Ativa'), ('Bloqueada', 'Bloqueada'), ('Cridada', 'Criada'), ('Encerrada', 'Encerrada')], max_length=25, verbose_name='Status')),
                ('qtd_encontro', models.PositiveIntegerField(blank=True, default=0, verbose_name='Quantidade de encontros')),
                ('atividade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='atividades.Atividade')),
                ('espacos_liberados', models.ManyToManyField(blank=True, to='academico.Espaco')),
                ('momento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academico.Momento')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turmas',
            },
        ),
    ]
