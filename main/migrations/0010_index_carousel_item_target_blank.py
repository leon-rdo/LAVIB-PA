# Generated by Django 4.2.5 on 2023-10-04 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_redes_sociais_icone_alter_curso_descricao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='index_carousel_item',
            name='target_blank',
            field=models.BooleanField(default=True, verbose_name='Abrir em outra guia?'),
        ),
    ]
