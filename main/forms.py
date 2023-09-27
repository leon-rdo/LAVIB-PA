from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import Curso, Evento, Inscrito
from django.forms.widgets import CheckboxSelectMultiple

class InscritoForm(ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border border-success', 'placeholder': 'dummy'}), label=_('Nome'))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control border border-success', 'placeholder': 'dummy'}), label=_('E-mail'))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border border-success', 'placeholder': 'dummy'}), label=_('Telefone'))
    graduacao = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border border-success', 'placeholder': 'dummy'}), label=_('Cursando'), help_text=_('Caso não esteja cursando nada, deixe em branco.'), required=False)
    instituicao = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border border-success', 'placeholder': 'dummy'}), label=_('Instituição'), help_text=_('Caso não esteja cursando nada, deixe em branco.'), required=False)
    cursos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'my-1'}),
        label=_('Selecione os cursos que deseja fazer:'),
        required=False,
        help_text=_('Verifique os preços na página anterior!')
    )

    def __init__(self, *args, **kwargs):
        evento_slug = kwargs.pop('evento_slug')
        super().__init__(*args, **kwargs)
        evento = get_object_or_404(Evento, slug=evento_slug)
        self.fields['cursos'].queryset = evento.cursos.all()

    class Meta:
        model = Inscrito
        fields = ['nome', 'email', 'telefone', 'graduacao', 'instituicao', 'cursos']

class ComprovanteForm(forms.Form):
    comprovante = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'})
    )

    class Meta:
            model = Inscrito
            fields = ['comprovante']