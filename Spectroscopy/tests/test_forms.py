from django.test import TestCase
from Spectroscopy.forms import UploadSpectrumForm

class UploadSpectrumFormTest(TestCase):

    def test_default(self):
        form=UploadSpectrumForm()
        self.assertIn('File', form.as_p())
