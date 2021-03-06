from SNe.tests.base import UnitTests
from SNe.models import SN
from Spectroscopy.models import Spectrum
from django.contrib import auth
from decouple import config

User=auth.get_user_model()
TEST_SPECTRUM=config('TEST_TOOLS')+'test_spectrum.txt'
SECOND_TEST_SPECTRUM=config('TEST_TOOLS')+'test_spectrum2.txt'


class SpectroscopyViewTest(UnitTests):

    def test_view_uses_spectroscopy_template_and_renders_form(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertTemplateUsed(response, 'Spectroscopy/spectroscopy.html')
        self.assertContains(response, 'SN 2017A')
        self.assertContains(response, "id_file")

    def test_uploading_file_redirects_back(self):
        sn=self.login_and_create_new_SN()
        myfile=open(TEST_SPECTRUM)
        response=self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        self.assertRedirects(response, '/sn/%d/spectroscopy/' % (sn.id))

    def test_view_renders_table(self):
        sn=self.login_and_create_new_SN()
        myfile=open(TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertContains(response, 'table-container')
        self.assertContains(response, '55055.0')

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        self.client.logout()
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertRedirects(response, "/?next=/sn/%d/spectroscopy/" % (sn.id))

class deleteSpectrumViewTest(UnitTests):

    def test_can_delete_spectrum_then_redirects_to_spectroscopy_page(self):
        sn=self.login_and_create_new_SN()
        myfile=open(TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        sp=Spectrum.objects.first()
        response=self.client.post('/sn/%d/spectroscopy/delete/' % (sn.id), data={'idlist': [str(sp.id)]})
        self.assertEqual(Spectrum.objects.count(), 0)
        self.assertRedirects(response, '/sn/%d/spectroscopy/' % (sn.id))

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        myfile=open(TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        sp=Spectrum.objects.first()
        self.client.logout()
        response=self.client.post('/sn/%d/spectroscopy/delete/' % (sn.id), data={'idlist': [str(sp.id)]})
        self.assertRedirects(response, '/?next=/sn/%d/spectroscopy/delete/' % (sn.id))

class queryViewTest(UnitTests):

    def test_query_returns_spectroscopy_data(self):
        sn=self.login_and_create_new_SN()
        myfile=open(TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        myfile=open(SECOND_TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55045.0, 'notes': ""})
        response=self.client.get('/sn/%d/spectroscopy/query/' % (sn.id))
        self.assertContains(response, "55055.0")
        self.assertContains(response, "55045.0")

    def test_query_returns_reference_date(self):
        sn = self.login_and_create_new_SN()
        sn.reference_date=55050.0
        sn.save()
        myfile = open(TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        response = self.client.get('/sn/%d/spectroscopy/query/' % (sn.id))
        self.assertContains(response, 55050.0)

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        myfile=open(TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55055.0, 'notes': ""})
        myfile=open(SECOND_TEST_SPECTRUM)
        self.client.post('/sn/%d/spectroscopy/' % (sn.id), {'file': myfile, 'MJD': 55045.0, 'notes': ""})
        self.client.logout()
        response=self.client.get('/sn/%d/spectroscopy/query/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/spectroscopy/query/' % (sn.id))
