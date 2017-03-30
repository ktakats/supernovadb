from django.test import TestCase
from SNe.models import SN
from Spectroscopy.models import Spectrum
from django.contrib import auth

User=auth.get_user_model()

def login_and_create_SN(self, name='SN 2017A', ra=22.625, dec=65.575):
    user=User.objects.create_user(username='test@test.com', password="bla")
    self.client.force_login(user)
    sn=SN.objects.create(sn_name=name, ra=ra, dec=dec, pi=user)
    return sn

class SpectroscopyViewTest(TestCase):

    def test_view_uses_spectroscopy_template_and_renders_form(self):
        sn=login_and_create_SN(self)
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertTemplateUsed(response, 'spectroscopy.html')
        self.assertContains(response, 'SN 2017A')
        self.assertContains(response, "id_file")

    def test_uploading_file_redirects_back(self):
        sn=login_and_create_SN(self)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        response=self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        self.assertRedirects(response, '/sn/%d/spectroscopy/' % (sn.id))

    def test_view_renders_table(self):
        sn=login_and_create_SN(self)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertContains(response, 'table-container')
        self.assertContains(response, '55055.0')

    def test_view_requires_login(self):
        sn=login_and_create_SN(self)
        self.client.logout()
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertRedirects(response, "/?next=/sn/%d/spectroscopy/" % (sn.id))

class deleteSpectrumViewTest(TestCase):

    def test_can_delete_spectrum_then_redirects_to_spectroscopy_page(self):
        sn=login_and_create_SN(self)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        sp=Spectrum.objects.first()
        response=self.client.get('/sn/%d/spectroscopy/delete/%d/' % (sn.id, sp.id))
        self.assertEqual(Spectrum.objects.count(), 0)
        self.assertRedirects(response, '/sn/%d/spectroscopy/' % (sn.id))

    def test_view_requires_login(self):
        sn=login_and_create_SN(self)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        sp=Spectrum.objects.first()
        self.client.logout()
        response=self.client.get('/sn/%d/spectroscopy/delete/%d/' % (sn.id, sp.id))
        self.assertRedirects(response, '/?next=/sn/%d/spectroscopy/delete/%d/' % (sn.id, sp.id))

class queryViewTest(TestCase):

    def test_query_returns_spectroscopy_data(self):
        sn=login_and_create_SN(self)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum2.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55045.0, 'notes': ""})
        response=self.client.get('/sn/%d/spectroscopy/query/' % (sn.id))
        self.assertContains(response, "55055.0")
        self.assertContains(response, "55045.0")

    def test_view_requires_login(self):
        sn=login_and_create_SN(self)
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        myfile=open('/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum2.dat')
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55045.0, 'notes': ""})
        self.client.logout()
        response=self.client.get('/sn/%d/spectroscopy/query/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/spectroscopy/query/' % (sn.id))
