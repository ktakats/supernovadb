from django.test import TestCase
from Photometry.models import Photometry
from SNe.models import SN

class PhotometryViewTest(TestCase):

    def test_view_uses_photometry_template(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/photometry/' % (sn.id))
        self.assertTemplateUsed(response, 'photometry.html')

    def test_view_renders_form(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/photometry/' % (sn.id))
        self.assertContains(response, "id_MJD")

    def test_view_renders_table(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.get('/sn/%d/photometry/' % (sn.id))
        self.assertContains(response, 'table-container')
        self.assertContains(response, '53003.5')

class editPhotViewTest(TestCase):

    def test_edit_fills_out_phot_form(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.get('/sn/%d/photometry/edit/%d/' % (sn.id, phot.id))
        form=response.context['form']
        self.assertIn('value="16.7"', form.as_p())

class deletePhotViewTest(TestCase):

    def test_can_delete_photometry_entry(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        phot=Photometry.objects.create(sn=sn, MJD=53003.5, Filter='V', magnitude=16.7, mag_error=0.02, notes="this sn")
        response=self.client.get('/sn/%d/photometry/delete/%d/' % (sn.id, phot.id))
        self.assertEqual(Photometry.objects.count(), 0)
