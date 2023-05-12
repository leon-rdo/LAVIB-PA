from django import forms


class CommentaryForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Insira seu nome aqui.",
            }
        )
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Deixe seu comentário aqui!",
                "rows": "3",
            }
        )
    )
