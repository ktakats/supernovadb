from django.test import TestCase
from SNe.models import SN
from Spectroscopy.models import Spectrum
from django.contrib import auth

User=auth.get_user_model()

class SpectroscopyTest(TestCase):

    def test_can_add_spectum(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        Sp=Spectrum.objects.create(sn=sn, MJD='55052.2', spectrum=[[0,0],[0,0]])
        Sp.save()
        self.assertEqual(Sp, Spectrum.objects.first())

    def test_can_add_data_points_to_spectrum(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        Sp=Spectrum.objects.create(sn=sn, MJD='55052.2', spectrum=[[3000.0, -15.0], [3005.0, -14.698970004336019]])
        self.assertEqual(len(Sp.spectrum), 2)
        self.assertEqual(Sp.spectrum[0][1], -15.0)
