from django import forms
from django.core.validators import RegexValidator


class ParserForm(forms.Form):
    link = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ссылка',
                'pattern': r'https://bgp.he.net/\w+'
            }
        ),
    )
