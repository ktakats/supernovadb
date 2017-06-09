from SNe.tests.base import UnitTests
from Photometry.models import Photometry
from Spectroscopy.models import Spectrum
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()


class PhotometryViewTest(UnitTests):

    def test_view_uses_photometry_template_renders_form(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/photometry/' % (sn.id))
        self.assertTemplateUsed(response, 'Photometry/photometry.html')
        self.assertContains(response, "id_MJD")

    def test_view_renders_table(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.get('/sn/%d/photometry/' % (sn.id))
        self.assertContains(response, 'table-container')
        self.assertContains(response, '53003.5')

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        self.client.logout()
        response=self.client.get('/sn/%d/photometry/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/photometry/' % (sn.id))

class editPhotViewTest(UnitTests):

    def test_edit_fills_out_phot_form(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.get('/sn/%d/photometry/edit/%d/' % (sn.id, phot.id))
        form=response.context['form']
        self.assertIn('value="16.7"', form.as_p())

    def test_redirects_to_phot_page_after_editing(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.post('/sn/%d/photometry/edit/%d/' % (sn.id, phot.id), data={'sn':sn, 'MJD':53003.5, 'Filter':'V', 'magnitude':15.7, 'mag_error': 0.02, 'notes': "this sn"})
        self.assertRedirects(response, '/sn/%d/photometry/' % (sn.id))

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        self.client.logout()
        response=self.client.post('/sn/%d/photometry/edit/%d/' % (sn.id, phot.id), data={'sn':sn, 'MJD':53003.5, 'Filter':'V', 'magnitude':15.7, 'mag_error': 0.02, 'notes': "this sn"})
        self.assertRedirects(response, '/?next=/sn/%d/photometry/edit/%d/' % (sn.id, phot.id),)


class deletePhotViewTest(UnitTests):

    def test_can_delete_photometry_entry(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.post('/sn/%d/photometry/delete/' % (sn.id), data={'idlist': [phot.id]})
        self.assertEqual(Photometry.objects.count(), 0)

    def test_can_delete_multiple_entry(self):
        sn=self.login_and_create_new_SN()
        phot1=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        phot2=Photometry.objects.create(sn=sn, MJD=53004.5, Filter='R', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.post('/sn/%d/photometry/delete/' % (sn.id), data={'idlist': [str(phot1.id)+','+str(phot2.id)]})
        self.assertEqual(Photometry.objects.count(), 0)

    def test_after_deletion_redirects_to_photometry_page(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.post('/sn/%d/photometry/delete/' % (sn.id), data={'idlist': [phot.id]})
        self.assertRedirects(response, '/sn/%d/photometry/' % (sn.id))

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        self.client.logout()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.post('/sn/%d/photometry/delete/' % (sn.id), data={'idlist': [phot.id]})
        self.assertRedirects(response, '/?next=/sn/%d/photometry/delete/' % (sn.id))
        self.assertEqual(Photometry.objects.count(),1)

class queryViewTest(UnitTests):

    def test_query_returns_photometry_data(self):
        sn=self.login_and_create_new_SN()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.get('/sn/%d/photometry/query/' % (sn.id))
        self.assertContains(response, "53003.50")

    def test_query_returns_reference_date(self):
        sn = self.login_and_create_new_SN()
        sn.reference_date="53000.5 (discovery)"
        sn.save()
        phot = Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02,                                       notes="this sn")
        response = self.client.get('/sn/%d/photometry/query/' % (sn.id))
        self.assertContains(response, 53000.5)

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        self.client.logout()
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.get('/sn/%d/photometry/query/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/photometry/query/' % (sn.id))

    def test_view_returns_list_of_spectra_taken(self):
        sn = self.login_and_create_new_SN()
        Sp = Spectrum.objects.create(sn=sn, MJD='55052.2', wavelength=[3000, 3500], flux=[-15, -16])
        Sp = Spectrum.objects.create(sn=sn, MJD='55055.2', wavelength=[3000, 3500], flux=[-15, -16])
        response = self.client.get('/sn/%d/photometry/query/' % (sn.id))
        self.assertContains(response, '55055.2')