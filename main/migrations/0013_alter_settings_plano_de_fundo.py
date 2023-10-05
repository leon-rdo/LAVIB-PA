# Generated by Django 4.2.5 on 2023-10-05 21:08

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_settings_plano_de_fundo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='plano_de_fundo',
            field=models.FileField(blank=True, null=True, upload_to='main/images', validators=[main.models.Settings.validate_media_file], verbose_name='Plano de fundo do site'),
        ),
    ]