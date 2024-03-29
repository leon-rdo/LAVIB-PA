# Generated by Django 4.2.1 on 2023-06-23 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LAVIB_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='lavib.pa@gmail.com', max_length=254)),
                ('telefone', models.CharField(default='91991487970', max_length=18)),
                ('qrcode_pagamento', models.ImageField(upload_to='main/images')),
                ('sobre_nos', models.TextField(default='')),
            ],
            options={
                'verbose_name': 'Informações da LAVIB',
                'verbose_name_plural': 'Informações da LAVIB',
            },
        ),
        migrations.CreateModel(
            name='RedesSocias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='', max_length=50)),
                ('icone', models.FileField(upload_to='main/images/RedesSociais')),
            ],
            options={
                'verbose_name': 'RedesSocias',
                'verbose_name_plural': 'RedesSocias',
            },
        ),
        migrations.DeleteModel(
            name='Contato',
        ),
        migrations.DeleteModel(
            name='QR_Code_Pagamento',
        ),
        migrations.DeleteModel(
            name='Sobre_Text',
        ),
    ]
