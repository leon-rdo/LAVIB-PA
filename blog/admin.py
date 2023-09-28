from django.contrib import admin
from blog.models import Post, Category

    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "creation_date"]
    list_filter = ["creation_date"]
    readonly_fields = ["creation_date", "last_modification"]

    fieldsets = [
        ('Informações do Post', {"fields": ['title', 'headline', 'body', 'image', 'autor', 'categories']}),
    ]

admin.site.register(Category)
