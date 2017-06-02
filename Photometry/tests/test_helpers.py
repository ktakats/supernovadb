from django.test import TestCase
from Photometry.helpers import uploadPhotometry
from SNe.models import SN
from django.contrib import auth
from decouple import config

User=auth.get_user_model()

class uploadPhotometryTest(TestCase):

    def test_reading_txt_file(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        filepath=config('TEST_TOOLS') + 'photometry.txt'
        myfile=open(filepath)
        response=self.client.post('/sn/%d/photometry/' % (sn.id), {'file': myfile})
        self.assertRedirects(response, '/sn/%d/photometry/' % (sn.id))

    def test_reading_dat_file(self):
        user = User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn = SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        filepath = config('TEST_TOOLS') + 'photometry.dat'
        myfile = open(filepath)
        response = self.client.post('/sn/%d/photometry/' % (sn.id), {'file': myfile})
        self.assertRedirects(response, '/sn/%d/photometry/' % (sn.id))