from django.test import TestCase
from Spectroscopy.forms import UploadSpectrumForm

class UploadSpectrumFormTest(TestCase):

    def test_default(self):
        form=UploadSpectrumForm()
        self.assertIn('File', form.as_p())

    def test_form_has_help_text(self):
        form=UploadSpectrumForm()
        self.assertIn("File needs two columns:\n First is wavelength, second is log10(Flux) (Do not use scientific notation!)\n Sparator is space", form.as_p())
