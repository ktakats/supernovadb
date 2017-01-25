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
        self.assertIn(sn.get_absolute_url(), '/%d/' % (sn.id))

    def test_coords_are_stored_properly(self):
        sn_added=SN.objects.create(sn_name='SN2017A', ra=83.866625, dec=-69.26986111)
        sn_indb=SN.objects.first()
        self.assertEqual(sn_indb, sn_added)
