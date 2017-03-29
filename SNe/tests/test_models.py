from __future__ import unicode_literals


from django.test import TestCase
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()

class SNModelTest(TestCase):

    def test_default_test(self):
        sn=SN()
        self.assertEqual(sn.sn_name, '')
        self.assertEqual(sn.ra, 0.0)
        self.assertEqual(sn.dec, 0.0)

    def test_can_create_object(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        self.assertEqual(sn, SN.objects.first())

    def test_get_absolute_url(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        self.assertIn(sn.get_absolute_url(), '/sn/%d/' % (sn.id))
