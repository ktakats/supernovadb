from django import forms

class UploadSpectrumForm(forms.Form):
    MJD=forms.DecimalField(max_digits=7, decimal_places=2)
    file=forms.FileField()
    notes=forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '3', 'cols': '25'}))
