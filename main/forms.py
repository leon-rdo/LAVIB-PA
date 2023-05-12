from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Evento, Inscrito

class InscritoForm(ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Nome'))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label=_('E-mail'))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Telefone'))
    curso = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Curso'))
    instituicao = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label=_('Instituição'))
    evento = forms.ModelChoiceField(
            queryset=Evento.objects.all(),
            empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'}),
            label=_('Evento')
        )

    class Meta:
        model = Inscrito
        fields = '__all__'
