# Generated by Django 2.1.1 on 2019-01-30 01:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
        ('atividades', '0003_auto_20181226_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='FotoAviso',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='Data de inclusão da foto')),
                ('data_alteracao', models.DateField(auto_now=True, verbose_name='Data de inclusão da foto')),
                ('ativo', models.BooleanField(blank=True, default=True, verbose_name='Ativo?')),
                ('foto', models.ImageField(null=True, upload_to='predios')),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contas.SuporteConta')),
            ],
            options={
                'verbose_name': 'Foto de aviso',
                'verbose_name_plural': 'Fotos de Avisos',
            },
        ),
    ]
