from datetime import date
from django.test import TestCase
from ObservationLogs.models import Obs
from ObservationLogs.forms import ObsLogForm
from SNe.models import SN

class ObsLogFormTest(TestCase):

    def test_default(self):
        form=ObsLogForm()
        self.assertIn('Setup', form.as_p())

    def test_form_validation(self):
        sn=SN.objects.create(sn_name='SN 2999A')
        form=ObsLogForm(data={'sn': sn, 'obs_date': date.today(), 'obs_type': 'S', 'telescope': 'ntt', 'instrument': 'EFOCS2', 'setup': 'gr11', 'notes': 'bla'})
        self.assertTrue(form.is_valid())

    def test_not_all_fields_are_required(self):
        sn=SN.objects.create(sn_name='SN 2999A')
        form=ObsLogForm(data={'sn': sn, 'obs_date': date.today(), 'telescope': 'ntt'})
        self.assertTrue(form.is_valid())

    def test_form_can_be_saved(self):
        sn=SN.objects.create(sn_name='SN 2999A')
        today=date.today()
        form=ObsLogForm(data={'sn': sn, 'obs_date': date.today(), 'telescope': 'ntt'})
        self.assertTrue(form.is_valid())
        form.save(sn=sn)
        obs=Obs.objects.get(obs_date=today)
        self.assertEqual('ntt', obs.telescope)

    def test_entry_is_updated_if_editing_it(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        obs=Obs.objects.create(sn=sn, obs_date=date.today(), obs_type= 'S', telescope= 'ntt', instrument= 'EFOCS2', setup= 'gr11', notes= 'bla')
        form=ObsLogForm(data={'sn': sn, 'obs_date': date.today(), 'obs_type': 'S', 'telescope': 'ntt', 'instrument': 'EFOCS2', 'setup': 'gr11, gr16', 'notes': 'bla'})
        self.assertTrue(form.is_valid())
        updated_obs=form.save(sn=sn, id=obs.id)
        self.assertEqual(obs.id, updated_obs.id)
