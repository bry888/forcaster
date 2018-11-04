from django import forms

class LinkForm(forms.Form):
    input_links = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 120}))
