import datetime
from django.utils import timezone
from uuid import uuid4
from django.db import models
from django.utils.text import slugify

class Index_Carousel_Item(models.Model):

    image = models.ImageField('Imagem', upload_to='main/images/indexCarousel')
    image_description = models.CharField('Descrição da Imagem', max_length=100, default='', help_text='Isto é importante para acessibilidade.')
    caption_title = models.CharField('Título da Notícia', max_length=50, default='')
    caption_text = models.CharField('Texto da Notícia', max_length=250, default='')
    link = models.URLField('Link da Notícia', default='')

    def __str__(self):
        return self.caption_title

    class Meta:
        verbose_name = 'Notícia'
        verbose_name_plural = 'Notícias'

class Diretor(models.Model):

    nome = models.CharField('Nome', max_length=60)
    foto = models.ImageField('Foto', upload_to='main/images/diretoria')
    ano = models.PositiveSmallIntegerField('Ano', default=datetime.date.today().year)
    lattes = models.URLField('Lattes', max_length=200, blank=True, null=True)
    linkedin = models.URLField('LinkedIn', max_length=200, blank=True, null=True)
    instagram = models.URLField('Instagram', max_length=200, blank=True, null=True)
    twitter = models.URLField('Twitter', max_length=200, blank=True, null=True)
    facebook = models.URLField('Facebook', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Diretor"
        verbose_name_plural = "Diretores"

class Patrocinador(models.Model):

    nome = models.CharField('Nome', max_length=20)
    imagem = models.ImageField('Imagem', upload_to='main/images/patrocinadores')
    link = models.URLField('Link', default='#', max_length=200)

    class Meta:
        verbose_name = "Patrocinador"
        verbose_name_plural = "Patrocinadores"

    def __str__(self):
        return self.nome

class Curso(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    imagem = models.ImageField('Imagem', upload_to='main/images/cursos')
    nome = models.CharField('Nome', max_length=50)
    descricao = models.CharField('Descrição', max_length=300)
    professor = models.CharField('Professor', max_length=100, blank=True, null=True, default=None)
    valor = models.DecimalField('Valor', max_digits=4, decimal_places=2)
    vagas = models.PositiveSmallIntegerField('Vagas', default=None, null=True, blank=True)
    
    @property
    def vagas_restantes(self):
        if self.vagas is None or self.vagas == '':
            return -1
        else:
            inscritos_count = self.inscritos.count()
            vagas_restantes = self.vagas - inscritos_count
            return vagas_restantes

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nome


class Desconto(models.Model):

    cupom = models.CharField('Cupom', max_length=25)
    valor = models.DecimalField('Valor', max_digits=4, decimal_places=2)
    quantidade = models.PositiveSmallIntegerField('Quantidade', null=True)
    
    @property
    def cupons_restantes(self):
        if self.quantidade is not None:
            cupons_usados = Inscrito.objects.filter(desconto=self).count()
            cupons_restantes = self.quantidade - cupons_usados
            return cupons_restantes
        else:
            return None
    
    class Meta:
        verbose_name = "Desconto"
        verbose_name_plural = "Descontos"

    def __str__(self):
        return self.cupom


class Evento(models.Model):
    
    titulo = models.CharField('Título', max_length=50)
    descricao_curta = models.CharField('Descrição curta', max_length=150)
    descricao = models.TextField('Descrição longa')
    mensagem_comprovante = models.CharField('Mensagem para o comprovante', default='Não se atrase!', max_length=150, null=True, blank=True)
    imagem = models.ImageField('Imagem', upload_to='main/images/eventos')
    data_hora = models.DateTimeField('Data e hora')
    local = models.CharField('Local', max_length=50)
    valor = models.DecimalField('Valor', max_digits=4, decimal_places=2)
    vagas = models.PositiveSmallIntegerField('Vagas', default=None, null=True, blank=True)
    carga_horaria = models.PositiveSmallIntegerField('Carga horária', default=0)
    convidados = models.CharField('Convidados', max_length=100, null=True, blank=True)
    cursos = models.ManyToManyField(Curso, verbose_name="Cursos", blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=False, editable=False)
    descontos = models.ManyToManyField(Desconto, verbose_name="Descontos", blank=True, default=None)

    @property
    def possui_cursos_pagos(self):
        return self.cursos.filter(valor__gt=0).exists()

    @property
    def vagas_restantes(self):
        if self.vagas is None or self.vagas == '':
            return -1
        else:
            inscritos_count = self.inscritos.count()
            vagas_restantes = self.vagas - inscritos_count
            return vagas_restantes

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Evento, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class Inscrito(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    numero_inscricao = models.PositiveSmallIntegerField('Nº')
    nome = models.CharField('Nome',default='', max_length=80)
    email = models.EmailField('E-mail', default='')
    telefone = models.CharField('Telefone', default='', max_length=18)
    graduacao = models.CharField('Cursando', max_length=50, null=True, blank=True)
    cursos = models.ManyToManyField(Curso, blank=True)
    instituicao = models.CharField('Instituição', null=True, blank=True, max_length=50)
    data_hora_inscricao = models.DateTimeField('Data da Inscrição', auto_now_add=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscritos')
    pagamento_confirmado = models.BooleanField('Pagou?', default=False)
    data_limite_pagamento = models.DateTimeField('Data limite de pagamento', null=True, blank=True)
    comprovante = models.ImageField(
        upload_to='main/images/comprovantes',
        null=True,
        blank=True,
    )
    desconto = models.ForeignKey(Desconto, verbose_name="Desconto", on_delete=models.CASCADE, blank=True, null=True, default=None)
    def save(self, *args, **kwargs):
        if not self.pk:
            # É uma nova instância, defina a data e hora limite para o pagamento como 24 horas a partir do momento atual
            self.data_limite_pagamento = timezone.now() + datetime.timedelta(hours=24)

        if not self.numero_inscricao:
            ultimo_numero = Inscrito.objects.filter(evento=self.evento).order_by('-numero_inscricao').first()
            if ultimo_numero:
                self.numero_inscricao = int(ultimo_numero.numero_inscricao) + 1
            else:
                self.numero_inscricao = 1

        super().save(*args, **kwargs)

    def verificar_pagamento(self):
        if self.pagamento_confirmado:
            # O pagamento já foi confirmado, não há necessidade de verificar
            return

        if self.data_limite_pagamento and timezone.now() > self.data_limite_pagamento:
            # A data e hora limite para o pagamento foram ultrapassadas, cancela a inscrição
            self.delete()

    class Meta:
        verbose_name = "Inscrito"
        verbose_name_plural = "Inscritos"
        unique_together = ('numero_inscricao', 'evento')
        unique_together = ('email', 'evento')

    def __str__(self):
        return self.evento.titulo

class Settings(models.Model):
    
    COLORS = (
        ('warning', 'Amarelo'),
        ('danger', 'Vermelho'),
        ('info', 'Azul'),
        ('secondary', 'Preto')
    )
    
    email = models.EmailField('E-mail', default='lavib.pa@gmail.com', max_length=254)
    telefone = models.CharField('Telefone', default='91991487970', max_length=18)
    chave_pix = models.CharField('Chave pix', max_length=50)
    qrcode_pagamento = models.ImageField('QR Code do Pix', upload_to='main/images')
    nome_conta = models.CharField('Nome do titular da conta', max_length=100)
    sobre_nos = models.TextField('Texto "Sobre nós"', blank=True)
    alerta_negrito = models.CharField('Texto em negrito do alerta', max_length=50, blank=True, null=True)
    alerta_text = models.CharField('Texto do alerta', max_length=100)
    alerta_cor = models.CharField('Cor do alerta', max_length=40, default='warning', choices=COLORS)
    alerta_link = models.URLField('Link do alerta', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Configurações'
        verbose_name_plural = 'Configurações'


class Redes_Sociais(models.Model):

    nome = models.CharField('Nome', default='', max_length=50)
    url = models.URLField('Link', default='', max_length=200)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Redes Sociais'
        verbose_name_plural = 'Redes Sociais'