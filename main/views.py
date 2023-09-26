import base64
import io
import json
import uuid
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from main.forms import ComprovanteForm, InscritoForm
from .models import *
import qrcode
from weasyprint import HTML
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class IndexView(generic.TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel_items"] = Index_Carousel_Item.objects.all()
        context["alertas"] = Alerta.objects.all()
        context["diretores"] = Diretor.objects.all()
        return context


class SobreView(generic.TemplateView):
    template_name = "main/sobre.html"

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

def enviar_email_html(destinatario, assunto, template_name, context):
    # Renderizar o template HTML em uma string
    html_content = render_to_string(template_name, context)

    # Remover as tags HTML para obter o conteúdo de texto
    text_content = strip_tags(html_content)

    # Criar uma instância de EmailMessage
    email = EmailMultiAlternatives(
        subject=assunto,
        body=text_content,
        to=[destinatario],
    )

    # Adicionar o conteúdo HTML como uma alternativa
    email.attach_alternative(html_content, "text/html")

    # Enviar o e-mail
    email.send()

class InscricaoView(generic.FormView):
    template_name = "main/inscricao.html"
    form_class = InscritoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento_slug = self.kwargs['evento_slug']
        evento = get_object_or_404(Evento, slug=evento_slug)
        context['evento'] = evento
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['evento_slug'] = self.kwargs['evento_slug']
        return kwargs
    
    def form_valid(self, form):
        inscrito = form.save(commit=False)
        evento_slug = self.kwargs['evento_slug']
        evento = get_object_or_404(Evento, slug=evento_slug)
        if Inscrito.objects.filter(email=inscrito.email, evento=evento).exists():
            return self.form_invalid(form, 'Inscrito com este e-mail já existe!')
        inscrito.evento = evento
        inscrito.save()

        inscrito.cursos.clear()
        inscrito.save()
        inscrito.cursos.set(form.cleaned_data['cursos'])

        # Define o pagamento como confirmado para o inscrito quando o evento e cursos são gratuitos
        valor_cursos = inscrito.cursos.aggregate(total=models.Sum('valor'))['total']
        if evento.valor == 0 and (valor_cursos is None or valor_cursos == 0):
            inscrito.pagamento_confirmado = True
            inscrito.save()

        destinatario = inscrito.email
        assunto = f'Comprovante de Inscrição - {evento.titulo}' if inscrito.pagamento_confirmado else f'Comprovante de Pré-Inscrição - {evento.titulo}'
        template_name = 'main/email_confirmacao.html'
        context = {
            'evento': evento,
            'inscrito': inscrito,
        }
        enviar_email_html(destinatario, assunto, template_name, context)

        comprovante_url = reverse('main:comprovante_inscricao', kwargs={'evento_slug': evento.slug})
        numero_inscricao = inscrito.numero_inscricao
        redirecionar_url = f"{comprovante_url}?numero_inscricao={numero_inscricao}"
        return redirect(redirecionar_url)
    
    def form_invalid(self, form, message):
        if message is not None:
            messages.error(self.request, message)
        else:
            messages.error(self.request, 'Algo deu errado!')
        return super().form_invalid(form)


def create_qr_code_image(json_data):
    # Cria o QR Code com os dados em formato JSON
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(json_data)
    qr.make(fit=True)

    # Renderiza o QR Code em uma imagem
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Converte a imagem em bytes
    image_bytes = io.BytesIO()
    qr_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    return image_bytes


class ComprovanteInscricaoView(generic.DetailView):
    template_name = 'main/comprovante_inscricao.html'
    template_name_imprimir = 'main/comprovante_imprimir.html'

    def get(self, request, evento_slug):
        numero_inscricao = request.GET.get('numero_inscricao')

        if not numero_inscricao:
            raise Http404

        inscrito = get_object_or_404(Inscrito, numero_inscricao=numero_inscricao, evento__slug=evento_slug)
        evento = get_object_or_404(Evento, slug=evento_slug)

        valor_evento = evento.valor
        valor_cursos = inscrito.cursos.aggregate(total=models.Sum('valor'))['total'] or 0
        valor_total = valor_evento + valor_cursos

        # Cria um objeto com os dados do participante
        participant_data = {
            "nome": inscrito.nome,
            "numero_inscricao": inscrito.numero_inscricao,
            "id": str(inscrito.id)
        }

        # Converte o objeto em uma string JSON
        json_data = json.dumps(participant_data)

        # Cria o QR Code e a imagem do QR Code
        qr_code_image = create_qr_code_image(json_data)

        # Passa o valor do QR Code como contexto para o template
        context = {
            'qr_code_inscricao': base64.b64encode(qr_code_image.read()).decode('utf-8'),
            'inscrito': inscrito,
            'evento': evento,
            'valor_total': valor_total,
            'comprovante_form': ComprovanteForm(),
        }

        if 'imprimir' in request.GET:
            # Renderiza o novo template com o contexto
            rendered_template = render_to_string(self.template_name_imprimir, context)

            # Cria um objeto HTML usando o conteúdo renderizado do template
            html = HTML(string=rendered_template)

            # Gera o PDF a partir do objeto HTML
            pdf_file = html.write_pdf()

            # Retorna o PDF como resposta HTTP para download
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Comprovante de Inscrição - LAVIB.pdf"'
            return response

        return render(request, self.template_name, context)

    def post(self, request, evento_slug):
        numero_inscricao = request.GET.get('numero_inscricao')

        if not numero_inscricao:
            raise Http404

        inscrito = get_object_or_404(Inscrito, numero_inscricao=numero_inscricao, evento__slug=evento_slug)
        evento = get_object_or_404(Evento, slug=evento_slug)

        comprovante_form = ComprovanteForm(request.POST, request.FILES)

        if comprovante_form.is_valid():
            comprovante_file = comprovante_form.cleaned_data['comprovante']
            inscrito.comprovante = comprovante_file
            inscrito.save()

            messages.success(request, '')

        valor_evento = evento.valor
        valor_cursos = inscrito.cursos.aggregate(total=models.Sum('valor'))['total'] or 0
        valor_total = valor_evento + valor_cursos

        # Cria um objeto com os dados do participante
        participant_data = {
            "nome": inscrito.nome,
            "numero_inscricao": inscrito.numero_inscricao,
            "id": str(inscrito.id)
        }

        # Converte o objeto em uma string JSON
        json_data = json.dumps(participant_data)

        # Cria o QR Code e a imagem do QR Code
        qr_code_image = create_qr_code_image(json_data)

        # Passa o valor do QR Code como contexto para o template
        context = {
            'qr_code_inscricao': base64.b64encode(qr_code_image.read()).decode('utf-8'),
            'inscrito': inscrito,
            'evento': evento,
            'valor_total': valor_total,
            'comprovante_form': comprovante_form,
        }

        return render(request, self.template_name, context)



class ConsultaInscricaoView(generic.FormView):
    template_name = "main/suas_inscricoes.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email', '')
        inscricoes = Inscrito.objects.filter(email=email)
        return render(request, self.template_name, {'inscricoes': inscricoes})


class PatrocinadoresView(generic.ListView):
    template_name = "main/patrocinadores.html"
    context_object_name = "patrocinadores"
    model = Patrocinador