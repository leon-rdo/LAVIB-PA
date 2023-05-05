from django.views import generic
from .models import Text

class IndexView(generic.ListView):
    model = Text
    template_name = "main/index.html"
    context_object_name = "texts"