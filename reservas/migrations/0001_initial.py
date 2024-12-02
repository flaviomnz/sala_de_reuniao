# Generated by Django 5.1.3 on 2024-11-30 15:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('capacidade', models.IntegerField()),
                ('recursos', models.TextField()),
                ('status', models.CharField(choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horario_inicio', models.DateTimeField()),
                ('horario_fim', models.DateTimeField()),
                ('status_reserva', models.CharField(choices=[('P', 'Pendente'), ('C', 'Confirmada')], default='P', max_length=1)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.sala')),
            ],
        ),
    ]
