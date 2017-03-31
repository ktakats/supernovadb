from django.test import TestCase
from django.contrib import auth
from SNe.models import SN
User=auth.get_user_model()


class UnitTests(TestCase):

    def login_and_create_new_SN(self, name='SN 2017A', ra=22.625, dec=65.575):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name=name, ra=ra, dec=dec, pi=user)
        return sn
