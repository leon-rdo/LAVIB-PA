from django.db import models
from django.utils.text import slugify
from datetime import datetime, timedelta


class Category(models.Model):
    category = models.CharField('Categoria', max_length=20)

    def __str__(self):
        return f"{self.category}"
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Post(models.Model):
    title = models.CharField('Título', max_length=255)
    headline = models.CharField('Manchete', max_length=255)
    body = models.TextField('Texto')
    image = models.ImageField('Imagem', upload_to='blog/images/big_images')
    creation_date = models.DateTimeField('Data de criação', auto_now_add=True)
    last_modification = models.DateTimeField('Última modificação', auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    slug = models.SlugField(max_length=100, unique=True, null=False, editable=False)
    autor = models.CharField('Autor', max_length=50, null=True, blank=True)

    def is_new_post(self):
        today = datetime.now().date()
        one_day_ago = today - timedelta(days=1)
        return self.creation_date.date() >= one_day_ago

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"