from django import forms
from django.core.exceptions import ValidationError
import magic

ALLOWED_FILE_TYPES=["text/plain"]

class UploadSpectrumForm(forms.Form):

    def validate_file_type(file):
        file.seek(0)
        file_type = magic.from_buffer(file.read(1024), mime=True)
        if file_type not in ALLOWED_FILE_TYPES:
            raise ValidationError("Incorrect file type")

    MJD=forms.DecimalField(max_digits=7, decimal_places=2)
    file=forms.FileField(validators=[validate_file_type,], help_text="File needs two columns:\n First is wavelength, second is log10(Flux) (Do not use scientific notation!)\n Sparator is space")
    notes=forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '3', 'cols': '25'}))
