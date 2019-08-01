# Generated by Django 2.1.1 on 2018-12-20 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academico', '0001_initial'),
        ('contas', '0001_initial'),
        ('atividades', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='turmaatividade',
            name='responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suporte_responsavel', to='contas.SuporteConta'),
        ),
        migrations.AddField(
            model_name='turmaatividade',
            name='softwares',
            field=models.ManyToManyField(blank=True, to='atividades.Software'),
        ),
        migrations.AddField(
            model_name='software',
            name='sistema',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividade_solicitante', to='atividades.SistemaOperacional'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='espaco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academico.Espaco'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atividades.TurmaAtividade'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='curso_setor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academico.CursoSetor'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contas.Solicitante'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='tipo_atividade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='atividades.TipoAtividade'),
        ),
    ]
