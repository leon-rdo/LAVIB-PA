# Generated by Django 4.2.5 on 2023-09-28 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_desconto_quantidade_alter_evento_descontos'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Alerta',
        ),
        migrations.AddField(
            model_name='settings',
            name='alerta_cor',
            field=models.CharField(choices=[('warning', 'Amarelo'), ('danger', 'Vermelho'), ('info', 'Azul'), ('secondary', 'Preto')], default='warning', max_length=40),
        ),
        migrations.AddField(
            model_name='settings',
            name='alerta_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='alerta_negrito',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='alerta_text',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
