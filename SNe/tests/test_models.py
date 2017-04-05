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
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        self.assertEqual(sn, SN.objects.first())

    def test_get_absolute_url(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        self.assertIn(sn.get_absolute_url(), '/sn/%d/' % (sn.id))

    def test_sn_can_have_multiple_co_is(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        coi1=User.objects.create_user(email='coi@test.com', password="blabla", first_name="CoTest")
        coi2=User.objects.create_user(email='coi2@test.com', password="blablabla", first_name="Co2Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=pi)
        sn.coinvestigators.add(coi1)
        sn.coinvestigators.add(coi2)
        sn.save()
        self.assertEqual(sn.coinvestigators.count(), 2)
        self.assertEqual(sn.coinvestigators.all()[0], coi1)
