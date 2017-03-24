from django.test import TestCase
from SNe.models import SN
from Spectroscopy.models import Spectrum

class SpectroscopyViewTest(TestCase):

    def test_view_uses_spectroscopy_template(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertTemplateUsed(response, 'spectroscopy.html')

    def test_view_returns_correct_sn_name(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertContains(response, 'SN 2017A')

    def test_view_renders_form(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertContains(response, "id_file")

    def test_uploading_file_redirects_back(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        response=self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        self.assertRedirects(response, '/sn/%d/spectroscopy/' % (sn.id))

    def test_view_renders_table(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertContains(response, 'table-container')
        self.assertContains(response, '55055.0')

class deleteSpectrumViewTest(TestCase):

    def test_can_delete_spectrum(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        sp=Spectrum.objects.first()
        response=self.client.get('/sn/%d/spectroscopy/delete/%d/' % (sn.id, sp.id))
        self.assertEqual(Spectrum.objects.count(), 0)

    def test_after_deletion_redirects_to_spectroscopy_page(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        sp=Spectrum.objects.first()
        response=self.client.get('/sn/%d/spectroscopy/delete/%d/' % (sn.id, sp.id))
        self.assertRedirects(response, '/sn/%d/spectroscopy/' % (sn.id))
