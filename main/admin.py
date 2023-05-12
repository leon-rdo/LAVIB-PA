from django.contrib import admin

from .models import *

class InscritoInline(admin.StackedInline):
    model = Inscrito
    extra = 1

class EventoAdmin(admin.ModelAdmin):
    inlines = [InscritoInline]


admin.site.register(Index_Carousel_Item)
admin.site.register(Text)
admin.site.register(Sobre_Text)
admin.site.register(Evento, EventoAdmin)

