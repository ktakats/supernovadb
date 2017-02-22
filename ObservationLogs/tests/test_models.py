from django.test import TestCase
from datetime import date
from ObservationLogs.models import Obs 
from SNe.models import SN

class ObservationTest(TestCase):

    def test_can_create_observation(self):
        today=date.today()
        sn=SN.objects.create(sn_name='SN 2017A')
        obs=Obs(sn=sn, obs_date=today, obs_type='S', telescope='NTT', instrument='EFOSC2', setup='GR13', notes='experimental')
        obs.save()
        self.assertEqual(obs, Obs.objects.first())
