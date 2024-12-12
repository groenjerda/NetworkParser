from django import forms


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
