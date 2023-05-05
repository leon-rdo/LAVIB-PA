from django.db import models


class Text(models.Model):
    short_text = models.CharField(max_length=200)

    def __str__(self):
        return self.short_text