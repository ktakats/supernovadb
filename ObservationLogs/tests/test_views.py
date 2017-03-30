from django.test import TestCase
from django_tables2 import RequestConfig
from datetime import date
from ObservationLogs.models import Obs
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()

class ObsLogViewTest(TestCase):

    def test_view_uses_obslog_template(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertTemplateUsed(response, 'obslog.html')

    def test_view_renders_form(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertContains(response, 'id_obs_date')

    def test_view_shows_observations_as_table(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertContains(response, "ntt")

    def test_view_requires_login(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        response=self.client.get('/sn/%d/obslog/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/obslog/' % (sn.id))

class DeleteObsViewTest(TestCase):

    def test_can_delete_observation(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertEqual(Obs.objects.count(), 0)

    def test_after_deletion_redirects_to_obslog_page(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertRedirects(response, '/sn/%d/obslog/' % (sn.id))

    def test_view_requires_login(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        self.client.logout()
        response=self.client.post('/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))
        self.assertRedirects(response, '/?next=/sn/%d/obslog/delete/%d/' % (sn.id, obs.id))

class EditObsViewTest(TestCase):

    def test_edit_fills_out_the_form(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.get('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id))
        form=response.context['form']
        self.assertIn('value="ntt"', form.as_p())

    def test_redirects_to_ObsLogView_after_editing(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        response=self.client.post('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id), data={'sn':sn, 'obs_date': date.today(), 'obs_type': 'S', 'telescope': 'ntt', 'instrument': 'EFOCS2', 'setup': 'gr11, gr16', 'notes': 'bla'})
        self.assertRedirects(response, '/sn/%d/obslog/' % (sn.id))

    def test_view_requires_login(self):
        user=User.objects.create_user(username='test@test.com', password="bla")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        self.client.logout()
        response=self.client.post('/sn/%d/obslog/edit/%d/' % (sn.id, obs.id), data={'sn':sn, 'obs_date': date.today(), 'obs_type': 'S', 'telescope': 'ntt', 'instrument': 'EFOCS2', 'setup': 'gr11, gr16', 'notes': 'bla'})
        self.assertRedirects(response, '/?next=/sn/%d/obslog/edit/%d/' % (sn.id, obs.id))
