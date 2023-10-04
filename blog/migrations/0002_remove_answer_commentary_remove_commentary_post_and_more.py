# Generated by Django 4.2.5 on 2023-09-28 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='commentary',
        ),
        migrations.RemoveField(
            model_name='commentary',
            name='post',
        ),
        migrations.DeleteModel(
            name='Forbidden_Word',
        ),
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(max_length=20, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='post',
            name='autor',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de criação'),
        ),
        migrations.AlterField(
            model_name='post',
            name='headline',
            field=models.CharField(max_length=255, verbose_name='Manchete'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='blog/images/big_images', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='post',
            name='last_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='Última modificação'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Título'),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Commentary',
        ),
    ]