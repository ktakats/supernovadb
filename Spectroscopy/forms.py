from django import forms

class UploadSpectrumForm(forms.Form):
    MJD=forms.DecimalField(max_digits=7, decimal_places=2)
    file=forms.FileField(help_text="File needs two columns:\n First is wavelength, second is log10(Flux) (Do not use scientific notation!)\n Sparator is space")
    notes=forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '3', 'cols': '25'}))
