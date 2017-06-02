from django.test import TestCase
from SNe.models import SN
from Spectroscopy.models import Spectrum
from django.contrib import auth
from decouple import config

User=auth.get_user_model()

class uploadSpectrumTest(TestCase):

    def test_helper_creates_data(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        filepath=config('TEST_TOOLS') + 'test_spectrum.txt'
        myfile=open(filepath)
        response=self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': 'test'})
        sp=Spectrum.objects.first()
        self.assertEqual(sp.MJD, 55055.0)
        wv=sp.wavelength
        self.assertEqual(wv[0]/1000., 3331.249)
        self.assertEqual(sp.notes, 'test')

    def test_helper_accepts_dat_files(self):
        user = User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn = SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        filepath = config('TEST_TOOLS') + 'test_spectrum2.dat'
        myfile = open(filepath)
        response = self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': 'test'})
        sp = Spectrum.objects.first()
        self.assertEqual(sp.MJD, 55055.0)
        wv = sp.wavelength
        self.assertEqual(wv[0] / 1000., 3351.072)
        self.assertEqual(sp.notes, 'test')

    def test_helper_accepts_ascii_files(self):
        user = User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn = SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        filepath = config('TEST_TOOLS') + 'test_spectrum2.ascii'
        myfile = open(filepath)
        response = self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': 'test'})
        sp = Spectrum.objects.first()
        self.assertEqual(sp.MJD, 55055.0)
        wv = sp.wavelength
        self.assertEqual(wv[0] / 1000., 3351.072)
        self.assertEqual(sp.notes, 'test')