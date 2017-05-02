from django.test import TestCase
from SNe.models import SN
from Spectroscopy.models import Spectrum, SpectrumDataPoint
from django.contrib import auth

User=auth.get_user_model()

class uploadSpectrumTest(TestCase):

    def test_helper_creates_data(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.txt')
        response=self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': 'test'})
        sp=Spectrum.objects.first()
        self.assertEqual(sp.MJD, 55055.0)
        p1=SpectrumDataPoint.objects.first()
        self.assertEqual(p1.wavelength, 3331.2495117188)
        self.assertEqual(sp.notes, 'test')
