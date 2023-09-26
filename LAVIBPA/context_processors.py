from main.models import Patrocinador, Settings

def patrocinadores(request):
    patrocinadores = Patrocinador.objects.all()
    return {'patrocinadores': patrocinadores}

def settings(request):
    settings = Settings.objects.first()
    return {'settings': settings}
