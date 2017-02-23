from django.test import TestCase
from django_tables2 import RequestConfig
from datetime import date
from ObservationLogs.models import Obs
from SNe.models import SN

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
        self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertEqual(Obs.objects.count(), 0)

    def test_after_deletion_redirects_to_obslog_page(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertRedirects(response, '/sn/%d/obslog/' % (sn.id))

class EditObsViewTest(TestCase):

    def test_edit_fills_out_the_form(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.get('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id))
        form=response.context['form']
        self.assertIn('value="ntt"', form.as_p())

    def test_redirects_to_ObsLogView_after_editing(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.post('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id), data={'sn':sn, 'obs_date': date.today(), 'obs_type': 'S', 'telescope': 'ntt', 'instrument': 'EFOCS2', 'setup': 'gr11, gr16', 'notes': 'bla'})
        self.assertRedirects(response, '/sn/%d/obslog/' % (sn.id))
