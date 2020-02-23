from django import forms

class blockliste(forms.Form):
    users = forms.TextField(label='Blockliste')
