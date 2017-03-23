from django import forms

class UploadSpectrumForm(forms.Form):
    file=forms.FileField()
