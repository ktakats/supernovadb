from django.test import TestCase
from Photometry.models import Photometry
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()

class PhotometryTest(TestCase):

    def test_can_create_photometric_point(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        phot=Photometry.objects.create(sn=sn, MJD=53005.0, Filter='B', magnitude=15.5, mag_error=002)
        phot.save()
        self.assertEqual(phot, Photometry.objects.first())
