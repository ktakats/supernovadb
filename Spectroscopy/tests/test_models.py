from django.test import TestCase
from SNe.models import SN
from Spectroscopy.models import Spectrum, SpectrumDataPoint

class SpectroscopyTest(TestCase):

    def test_can_add_spectum(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        Sp=Spectrum.objects.create(sn=sn, MJD='55052.2')
        Sp.save()
        self.assertEqual(Sp, Spectrum.objects.first())

    def test_can_add_data_points_to_spectrum(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        Sp=Spectrum.objects.create(sn=sn, MJD='55052.2')
        p1=SpectrumDataPoint.objects.create(spectrum=Sp, wavelength=3000.0, flux=-15.0)
        p2=SpectrumDataPoint.objects.create(spectrum=Sp, wavelength=3005.0, flux=-14.698970004336019)
        points=SpectrumDataPoint.objects.filter(spectrum=Sp)
        self.assertEqual(len(points), 2)
        self.assertEqual(points[0].flux, p1.flux)
