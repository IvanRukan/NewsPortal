from django import forms


class NewsForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField()
