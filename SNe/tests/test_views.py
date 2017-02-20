from astropy import units as u
from astropy.coordinates import SkyCoord
from django.test import TestCase
from SNe.models import SN, Obs, Photometry
from datetime import date


class HomeViewTest(TestCase):

    def test_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class SNViewTest(TestCase):

    def test_view_uses_sn_template(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertTemplateUsed(response, 'sn.html')

    def test_view_shows_the_name_and_coordinates_of_sn(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'SN 2017A')
        self.assertContains(response, 'RA=01:30:30.000')
        self.assertContains(response, 'Dec=65:34:30.00')

    def test_view_has_link_to_obslog(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Observation log')

    def test_view_has_link_to_photometry(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Photometry')



class AddNewSNViewTest(TestCase):

    def test_uses_new_sn_template(self):
        response=self.client.get('/add_sn/')
        self.assertTemplateUsed(response, 'new_sn.html')

    def test_new_sn_page_renders_form(self):
        response=self.client.get('/add_sn/')
        self.assertContains(response, 'id_sn_name')

    def test_form_creates_new_database_entry(self):
        self.client.post('/add_sn/', data={'sn_name': 'SN 1999A', 'ra': '01:23:45.6', 'dec': '+65:34:27.3'})
        sn=SN.objects.first()
        c=SkyCoord('01:23:45.6', '+65:34:27.3', unit=(u.hourangle, u.deg))
        self.assertEqual(sn.sn_name, 'SN 1999A')
        self.assertEqual('%.2f' % (sn.ra), '%.2f' %  (c.ra.deg))
        self.assertEqual('%.2f' % (sn.dec), '%.2f' % (c.dec.deg))

    def test_form_submission_redirects_to_sn_page(self):
        response=self.client.post('/add_sn/', data={'sn_name': 'SN 1999A', 'ra': '01:23:45.6', 'dec': '+65:34:27.3'})
        sn=SN.objects.first()
        self.assertRedirects(response, '/sn/%d/' % (sn.id))

class ObsLogViewTest(TestCase):

    def test_view_uses_obslog_template(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertTemplateUsed(response, 'obslog.html')

    def test_view_renders_form(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertContains(response, 'id_obs_date')

    def test_view_shows_observations_as_table(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertContains(response, "ntt")



class DeleteObsViewTest(TestCase):

    def test_can_delete_observation(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        self.client.get('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertEqual(Obs.objects.count(), 0)

class EditObsViewTest(TestCase):

    def test_edit_fills_out_the_form(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.get('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id))
        form=response.context['form']
        self.assertIn('value="ntt"', form.as_p())

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
