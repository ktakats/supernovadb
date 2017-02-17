from django.test import TestCase
from SNe.models import SN
from SNe.models import Obs
from SNe.models import Photometry
from datetime import date

class SNModelTest(TestCase):

    def test_default_test(self):
        sn=SN()
        self.assertEqual(sn.sn_name, '')
        self.assertEqual(sn.ra, 0.0)
        self.assertEqual(sn.dec, 0.0)

    def test_can_create_object(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        self.assertEqual(sn, SN.objects.first())

    def test_get_absolute_url(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        self.assertIn(sn.get_absolute_url(), '/sn/%d/' % (sn.id))

class ObservationTest(TestCase):

    def test_can_create_observation(self):
        today=date.today()
        sn=SN.objects.create(sn_name='SN 2017A')
        obs=Obs(sn=sn, obs_date=today, obs_type='S', telescope='NTT', instrument='EFOSC2', setup='GR13', notes='experimental')
        obs.save()
        self.assertEqual(obs, Obs.objects.first())

class PhotometryTest(TestCase):

    def test_can_create_photometric_point(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        phot=Photometry.objects.create(sn=sn, MJD=53005.0, Filter='B', magnitude=15.5)
        phot.save()
        self.assertEqual(phot, Photometry.objects.first())
