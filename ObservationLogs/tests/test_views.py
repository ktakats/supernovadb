from SNe.tests.base import UnitTests
from django_tables2 import RequestConfig
from datetime import date
from ObservationLogs.models import Obs
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()




class ObsLogViewTest(UnitTests):

    def test_view_uses_obslog_template(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertTemplateUsed(response, 'ObservationLogs/obslog.html')

    def test_view_renders_form(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertContains(response, 'id_obs_date')

    def test_view_shows_observations_as_table(self):
        sn=self.login_and_create_new_SN()
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertContains(response, "ntt")

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        self.client.logout()
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/obslog/' % (sn.id))

class DeleteObsViewTest(UnitTests):

    def test_can_delete_observation(self):
        sn=self.login_and_create_new_SN()
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertEqual(Obs.objects.count(), 0)

    def test_after_deletion_redirects_to_obslog_page(self):
        sn=self.login_and_create_new_SN()
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertRedirects(response, '/sn/%d/obslog/' % (sn.id))

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        self.client.logout()
        response=self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertRedirects(response, '/?next=/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))

class EditObsViewTest(UnitTests):

    def test_edit_fills_out_the_form(self):
        sn=self.login_and_create_new_SN()
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.get('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id))
        form=response.context['form']
        self.assertIn('value="ntt"', form.as_p())

    def test_redirects_to_ObsLogView_after_editing(self):
        sn=self.login_and_create_new_SN()
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.post('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id), data={'sn':sn, 'obs_date': date.today(), 'obs_type': 'S', 'telescope': 'ntt', 'instrument': 'EFOCS2', 'setup': 'gr11, gr16', 'notes': 'bla'})
        self.assertRedirects(response, '/sn/%d/obslog/' % (sn.id))

    def test_view_requires_login(self):
        sn=self.login_and_create_new_SN()
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        self.client.logout()
        response=self.client.post('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id), data={'sn':sn, 'obs_date': date.today(), 'obs_type': 'S', 'telescope': 'ntt', 'instrument': 'EFOCS2', 'setup': 'gr11, gr16', 'notes': 'bla'})
        self.assertRedirects(response, '/?next=/sn/%d/obslog/edit/%d/' % (sn.id, obs.id))
