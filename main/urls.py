from . import views
from django.urls import path

app_name = "main"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("sobre/", views.SobreView.as_view(), name="sobre"),
    path("eventos/", views.EventosView.as_view(), name="eventos"),
    path("eventos/suas-inscricoes/", views.ConsultaInscricaoView.as_view(), name="suas_inscricoes"),
    path("eventos/<slug:evento_slug>/", views.DetalhesEventosView.as_view(), name="detalhes_eventos"),
    path("eventos/<slug:evento_slug>/inscricao/", views.InscricaoView.as_view(), name="inscricao"),
    path("eventos/<slug:evento_slug>/inscricao/comprovante/", views.ComprovanteInscricaoView.as_view(), name="comprovante_inscricao"),
    path("patrocinadores/", views.PatrocinadoresView.as_view(), name="patrocinadores"),
]