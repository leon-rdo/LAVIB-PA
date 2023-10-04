# Generated by Django 4.2.5 on 2023-09-28 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_delete_alerta_settings_alerta_cor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redes_sociais',
            name='icone',
        ),
        migrations.AlterField(
            model_name='curso',
            name='descricao',
            field=models.CharField(max_length=300, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='imagem',
            field=models.ImageField(upload_to='main/images/cursos', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='nome',
            field=models.CharField(max_length=50, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='professor',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Professor'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='vagas',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True, verbose_name='Vagas'),
        ),
        migrations.AlterField(
            model_name='curso',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='desconto',
            name='quantidade',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='ano',
            field=models.PositiveSmallIntegerField(default=2023, verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='facebook',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='foto',
            field=models.ImageField(upload_to='main/images/diretoria', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='instagram',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='lattes',
            field=models.URLField(blank=True, null=True, verbose_name='Lattes'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='linkedin',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='nome',
            field=models.CharField(max_length=60, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='diretor',
            name='twitter',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='carga_horaria',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Carga horária'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='convidados',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Convidados'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='data_hora',
            field=models.DateTimeField(verbose_name='Data e hora'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='descricao',
            field=models.TextField(verbose_name='Descrição longa'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='descricao_curta',
            field=models.CharField(max_length=150, verbose_name='Descrição curta'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='imagem',
            field=models.ImageField(upload_to='main/images/eventos', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='local',
            field=models.CharField(max_length=50, verbose_name='Local'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='mensagem_comprovante',
            field=models.CharField(blank=True, default='Não se atrase!', max_length=150, null=True, verbose_name='Mensagem para o comprovante'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='titulo',
            field=models.CharField(max_length=50, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='vagas',
            field=models.PositiveSmallIntegerField(blank=True, default=None, null=True, verbose_name='Vagas'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='index_carousel_item',
            name='caption_text',
            field=models.CharField(default='', max_length=250, verbose_name='Texto da Notícia'),
        ),
        migrations.AlterField(
            model_name='index_carousel_item',
            name='caption_title',
            field=models.CharField(default='', max_length=50, verbose_name='Título da Notícia'),
        ),
        migrations.AlterField(
            model_name='index_carousel_item',
            name='image',
            field=models.ImageField(upload_to='main/images/indexCarousel', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='index_carousel_item',
            name='image_description',
            field=models.CharField(default='', help_text='Isto é importante para acessibilidade.', max_length=100, verbose_name='Descrição da Imagem'),
        ),
        migrations.AlterField(
            model_name='index_carousel_item',
            name='link',
            field=models.URLField(default='', verbose_name='Link da Notícia'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='data_hora_inscricao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data da Inscrição'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='data_limite_pagamento',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data limite de pagamento'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='graduacao',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Cursando'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='instituicao',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Instituição'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='nome',
            field=models.CharField(default='', max_length=80, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='inscrito',
            name='telefone',
            field=models.CharField(default='', max_length=18, verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='patrocinador',
            name='imagem',
            field=models.ImageField(upload_to='main/images/patrocinadores', verbose_name='Imagem'),
        ),
        migrations.AlterField(
            model_name='patrocinador',
            name='link',
            field=models.URLField(default='#', verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='patrocinador',
            name='nome',
            field=models.CharField(max_length=20, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='redes_sociais',
            name='nome',
            field=models.CharField(default='', max_length=50, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='redes_sociais',
            name='url',
            field=models.URLField(default='', verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='alerta_cor',
            field=models.CharField(choices=[('warning', 'Amarelo'), ('danger', 'Vermelho'), ('info', 'Azul'), ('secondary', 'Preto')], default='warning', max_length=40, verbose_name='Cor do alerta'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='alerta_link',
            field=models.URLField(blank=True, null=True, verbose_name='Link do alerta'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='alerta_negrito',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Texto em negrito do alerta'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='alerta_text',
            field=models.CharField(max_length=100, verbose_name='Texto do alerta'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='chave_pix',
            field=models.CharField(max_length=50, verbose_name='Chave pix'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='email',
            field=models.EmailField(default='lavib.pa@gmail.com', max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='nome_conta',
            field=models.CharField(max_length=100, verbose_name='Nome do titular da conta'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='qrcode_pagamento',
            field=models.ImageField(upload_to='main/images', verbose_name='QR Code do Pix'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='sobre_nos',
            field=models.TextField(blank=True, verbose_name='Texto "Sobre nós"'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='telefone',
            field=models.CharField(default='91991487970', max_length=18, verbose_name='Telefone'),
        ),
    ]