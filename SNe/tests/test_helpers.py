from django.test import TestCase
from SNe.models import SN
from SNe.helpers import uploadPhotometry

class uploadPhotometryTest(TestCase):

    def test_reading_file(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry.txt')
        response=self.client.post('/sn/%d/photometry/' % (sn.id), {'file': myfile})
        self.assertContains(response, '55189.0')
