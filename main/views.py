from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View, generic
from main.forms import InscritoForm
from .models import *


class IndexView(generic.ListView):
    template_name = "main/index.html"

    model = Text
    model = Index_Carousel_Item
    
    context_object_name = "texts"
    context_object_name = "carousel_items"

class SobreView(generic.ListView):
    template_name = "main/sobre.html"

    model = Sobre_Text
    
    context_object_name = "sobre_texts"

class EventosView(generic.ListView):
    template_name = "main/eventos.html"

    model = Evento
    
    context_object_name = "eventos"

class DetalhesEventosView(generic.DetailView):
    template_name = "main/detalhes_eventos.html"

    model = Evento
    
    context_object_name = "evento"

    slug_field = 'slug'
    slug_url_kwarg = 'evento_slug'


class InscricaoView(generic.FormView):
    template_name = "main/inscricao.html"

    form_class = InscritoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = get_object_or_404(Evento, slug=self.kwargs['evento_slug'])
        context['evento'] = evento
        return context

    def form_valid(self, form):
        inscrito = form.save(commit=False)
        inscrito.evento = Evento.objects.get(slug=self.kwargs['evento_slug'])
        inscrito.save()
        url = reverse('main:comprovante_inscricao', args=(inscrito.evento.slug, inscrito.id))
        return redirect(url)

class ComprovanteInscricaoView(View):
    template_name = 'main/comprovante_inscricao.html'

    def get(self, request, evento_slug, inscrito_id):
        inscrito = get_object_or_404(Inscrito, id=inscrito_id, evento__slug=evento_slug)
        evento = get_object_or_404(Evento, slug=evento_slug)
        return render(request, self.template_name, {'inscrito': inscrito, 'evento': evento})