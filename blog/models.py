from django.db import models
from django.utils.text import slugify
from datetime import datetime, timedelta


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Post(models.Model):
    title = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to='blog/images/big_images')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')
    slug = models.SlugField(max_length=100, unique=True, null=False, editable=False)
    autor = models.CharField(max_length=50, null=True, blank=True)

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


class Commentary(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def comment(self):
        return self.body.split()[:5]

    class Meta:
        verbose_name_plural = "commentaries"

class Answer(models.Model):
    administrador = models.CharField(max_length=50, null=True, blank=True)
    resposta = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    commentary = models.ForeignKey('Commentary', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"


class Forbidden_Word(models.Model):
    word = models.CharField(max_length=15)