from django.test import TestCase
from Photometry.models import Photometry
from SNe.models import SN

class PhotometryTest(TestCase):

    def test_can_create_photometric_point(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        phot=Photometry.objects.create(sn=sn, MJD=53005.0, Filter='B', magnitude=15.5, mag_error=002)
        phot.save()
        self.assertEqual(phot, Photometry.objects.first())
