from django.test import TestCase
from Photometry.helpers import uploadPhotometry
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()

class uploadPhotometryTest(TestCase):

    def test_reading_file(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry.txt')
        response=self.client.post('/sn/%d/photometry/' % (sn.id), {'file': myfile})
        self.assertRedirects(response, '/sn/%d/photometry/' % (sn.id))
