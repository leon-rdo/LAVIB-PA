from main.models import Patrocinador, Settings, Redes_Sociais

def patrocinadores(request):
    patrocinadores = Patrocinador.objects.all()
    return {'patrocinadores': patrocinadores}

def settings(request):
    settings = Settings.objects.first()
    return {'settings': settings}

def redes_sociais(request):
    redes_sociais = Redes_Sociais.objects.all()
    return {'redes_sociais': redes_sociais}