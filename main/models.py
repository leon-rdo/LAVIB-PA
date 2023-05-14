from datetime import timezone
from uuid import uuid4
from django.db import models
from django.utils.text import slugify

class Text(models.Model):
    short_text = models.CharField(max_length=200)

    def __str__(self):
        return self.short_text
    
class Index_Carousel_Item(models.Model):

    image = models.ImageField(upload_to='main/images/indexCarousel')
    image_description = models.CharField(max_length=100, default='')
    caption_title = models.CharField(max_length=50, default='')
    caption_text = models.CharField(max_length=250, default='')
    link = models.URLField(default='')

    def __str__(self):
        return self.caption_title

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Index_Carousel_Item'
        verbose_name_plural = 'Index_Carousel_Items'

class Sobre_Text(models.Model):
    
    paragraph = models.TextField(default='')    

    class Meta:
        verbose_name = "Sobre_Text"
        verbose_name_plural = "Sobre_Texts"


class Evento(models.Model):
    titulo = models.CharField(max_length=50)
    descricao_curta = models.CharField(max_length=150)
    descricao = models.TextField()
    mensagem_comprovante = models.CharField(default='Não se atrase!', max_length=150, null=True, blank=True)
    imagem = models.ImageField(upload_to='main/images/eventos')
    data_hora = models.DateTimeField()
    local = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=4, decimal_places=2)
    vagas = models.PositiveSmallIntegerField(default=None, null=True, blank=True)
    carga_horaria = models.PositiveSmallIntegerField(default=0)
    convidados = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=False, editable=False)

    def vagas_restantes(self):
        if self.vagas is None or self.vagas == '':
            # Evento com vagas ilimitadas
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
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True, db_column='token_acesso')
    numero_inscricao = models.PositiveSmallIntegerField()
    nome = models.CharField(default='', max_length=80)
    email = models.EmailField(default='')
    telefone = models.CharField(default='', max_length=18)
    curso = models.CharField(null=True, blank=True, max_length=50)
    instituicao = models.CharField(null=True, blank=True, max_length=50)
    data_hora_inscricao = models.DateTimeField(auto_now_add=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscritos')
    pagamento_confirmado = models.BooleanField(default=False)
    data_limite_pagamento = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # É uma nova instância, defina a data e hora limite para o pagamento como 24 horas a partir do momento atual
            self.data_limite_pagamento = timezone.now() + timezone.timedelta(hours=24)

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
        return f"Inscrição #{str(self.numero_inscricao)} - {self.nome}"

    
class Alerta(models.Model):

    COLORS = (
        ('warning', 'Amarelo'),
        ('danger', 'Vermelho'),
        ('info', 'Azul'),
        ('secondary', 'Preto')
    )

    negrito = models.CharField(max_length=50, blank=True, null=True)
    texto = models.CharField(max_length=100)
    cor = models.CharField(max_length=40, default='warning', choices=COLORS)

    class Meta:
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"

    def __str__(self):
        return self.negrito