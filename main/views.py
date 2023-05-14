from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View, generic
from main.forms import InscritoForm
from .models import *


class IndexView(generic.ListView):
    template_name = "main/index.html"
    
    context_object_name = "texts"
    queryset = Text.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel_items"] = Index_Carousel_Item.objects.all()
        context["alerta"] = Alerta.objects.all()
        return context


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
        evento_slug = self.kwargs['evento_slug']
        evento = get_object_or_404(Evento, slug=evento_slug)
        inscrito.evento = evento
        inscrito.save()

        return render(self.request, 'main/comprovante_inscricao.html', {'inscrito': inscrito, 'evento': evento})

class ComprovanteInscricaoView(View):
    template_name = 'main/comprovante_inscricao.html'

    def get(self, request, evento_slug):
        numero_inscricao = request.GET.get('numero_inscricao')

        if not numero_inscricao:
            raise Http404

        inscrito = get_object_or_404(Inscrito, numero_inscricao=numero_inscricao, evento__slug=evento_slug)
        evento = get_object_or_404(Evento, slug=evento_slug)
        return render(request, self.template_name, {'inscrito': inscrito, 'evento': evento})
    
class ConsultaInscricaoView(View):
    template_name = "main/suas_inscricoes.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', '')
        inscricoes = Inscrito.objects.filter(email=email)
        return render(request, self.template_name, {'inscricoes': inscricoes})