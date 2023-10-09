import datetime
from django.forms import ValidationError
from uuid import uuid4
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Index_Carousel_Item(models.Model):

    image = models.ImageField('Imagem', upload_to='main/images/indexCarousel')
    image_description = models.CharField('Descrição da Imagem', max_length=100, default='', help_text='Isto é importante para acessibilidade.')
    caption_title = models.CharField('Título da Notícia', max_length=50, default='')
    caption_text = models.CharField('Texto da Notícia', max_length=250, default='')
    link = models.URLField('Link da Notícia', default='')
    target_blank = models.BooleanField('Abrir em outra guia?', default=True)

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
    
    def get_absolute_url(self):
        return reverse("main:patrocinadores")
    

class Participante(models.Model):
    
    nome = models.CharField('Nome', max_length=100)
    descricao = models.CharField('Descrição', max_length=255)
    foto = models.ImageField('Foto', upload_to='main/images/participantes')

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"

    def __str__(self):
        return self.nome


class Curso(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    imagem = models.ImageField('Imagem', upload_to='main/images/cursos')
    nome = models.CharField('Nome', max_length=50)
    descricao = models.CharField('Descrição', max_length=300)
    professor = models.ManyToManyField(Participante, blank=True)
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
    data_hora_final = models.DateTimeField('Data e hora do fim do evento')
    local = models.CharField('Local', max_length=50)
    valor = models.DecimalField('Valor', max_digits=4, decimal_places=2)
    vagas = models.PositiveSmallIntegerField('Vagas', default=None, null=True, blank=True)
    carga_horaria = models.PositiveSmallIntegerField('Carga horária', default=0)
    palestrantes = models.ManyToManyField(Participante, blank=True)
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
        
    def clean(self):
        """
        Validação personalizada para garantir que a data final seja maior que a data inicial.
        """
        if self.data_hora and self.data_hora_final:
            if self.data_hora >= self.data_hora_final:
                raise ValidationError("A data final deve ser maior que a data inicial.")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Evento, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("main:detalhes_eventos", kwargs={"evento_slug": self.slug})


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
    comprovante = models.ImageField(upload_to='main/images/comprovantes', null=True, blank=True)
    indicacao = models.CharField('Quem indicou?', max_length=70, null=True, blank=True)
    desconto = models.ForeignKey(Desconto, verbose_name="Desconto", on_delete=models.CASCADE, blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Inscrito"
        verbose_name_plural = "Inscritos"
        unique_together = ('numero_inscricao', 'evento')
        unique_together = ('email', 'evento')

    def __str__(self):
        return self.evento.titulo
    
    def get_absolute_url(self):
        url = reverse("main:comprovante_inscricao", kwargs={"evento_slug": self.evento.slug})
        url += f"?numero_inscricao={self.numero_inscricao}"
        return url
    

class Settings(models.Model):
    
    COLORS = (
        ('warning', 'Amarelo'),
        ('danger', 'Vermelho'),
        ('info', 'Azul'),
        ('secondary', 'Preto')
    )

    def validate_media_file(value):
        extension = value.name.split('.')[-1].lower()
        if extension not in ['jpg', 'jpeg', 'png', 'svg']:
            raise ValidationError("O arquivo deve ser uma imagem (jpg, jpeg, png, svg).")
    
    email = models.EmailField('E-mail', default='lavib.pa@gmail.com', max_length=254)
    telefone = models.CharField('Telefone', default='91991487970', max_length=18)
    chave_pix = models.CharField('Chave pix', max_length=50)
    qrcode_pagamento = models.ImageField('QR Code do Pix', upload_to='main/images')
    nome_conta = models.CharField('Nome do titular da conta', max_length=100)
    sobre_nos = models.TextField('Texto "Sobre nós"', blank=True)
    plano_de_fundo = models.FileField("Plano de fundo do site", upload_to='main/images', blank=True, null=True, validators=[validate_media_file])
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