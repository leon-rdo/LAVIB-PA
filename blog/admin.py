from django.contrib import admin
from blog.models import Post, Category, Commentary, Forbidden_Word, Answer

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0

class CommentaryInline(admin.TabularInline):
    model = Commentary
    extra = 1
    inlines = [AnswerInline]

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "creation_date"]
    list_filter = ["creation_date"]
    inlines = [
        CommentaryInline,
    ]

class CommentaryAdmin(admin.ModelAdmin):
    list_display = ["author", "comment", 'post', "creation_date"]
    list_filter = ["creation_date"]
    inlines = [
        AnswerInline,
    ]

admin.site.register(Post, PostAdmin)
admin.site.register(Commentary, CommentaryAdmin)
admin.site.register(Category)
admin.site.register(Forbidden_Word)
