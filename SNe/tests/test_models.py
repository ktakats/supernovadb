from django.test import TestCase
from SNe.models import SN

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
