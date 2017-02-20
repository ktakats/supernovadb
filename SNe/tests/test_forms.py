from django.test import TestCase
from SNe.forms import NewSNForm, ObsLogForm, PhotometryForm, UploadPhotometryFileForm
from SNe.models import SN, Obs, Photometry
from datetime import date

class NewSNFormTest(TestCase):

    def test_form_has_placeholders(self):
        form=NewSNForm()
        self.assertIn('00:00:00.00', form.as_p())

    def test_form_validation_for_blank_items(self):
        form=NewSNForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['sn_name'], ['You need to provide the name of the SN'])

    def test_form_validation_for_coords(self):
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '01:34:56.78', 'dec': '-69:53:24.6'})
        self.assertTrue(form.is_valid())

    def test_coords_are_saved_to_database(self):
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '01:34:56.78', 'dec': '-69:53:24.6'})
        self.assertTrue(form.is_valid())
        form.save()
        sn=SN.objects.get(sn_name='SN 2999A')
        self.assertEqual(sn.ra, 23.7365833333333)

    def test_invalid_coordinate_format_gives_error(self):
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '01:4:56.78', 'dec': '-69:53:24'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ra'], ['Incorrect coordinate format'])
        self.assertEqual(form.errors['dec'], ['Incorrect coordinate format'])

    def test_invalid_ra_gives_error(self):
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '25:45:56.78', 'dec': '-69:53:24.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ra'], ['Invalid coordinate value'])

        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '23:65:56.78', 'dec': '-69:53:24.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ra'], ['Invalid coordinate value'])

        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '23:55:66.78', 'dec': '-69:53:24.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ra'], ['Invalid coordinate value'])

    def test_invalid_dec_gives_error(self):
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '23:45:56.78', 'dec': '91:53:24.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dec'], ['Invalid coordinate value'])

        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '23:55:56.78', 'dec': '-95:53:24.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dec'], ['Invalid coordinate value'])

        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '23:55:56.78', 'dec': '-69:63:24.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dec'], ['Invalid coordinate value'])

        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '23:55:56.78', 'dec': '-69:53:65.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['dec'], ['Invalid coordinate value'])

    def test_cannot_duplicate_sn(self):
        sn=SN.objects.create(sn_name='SN 2999A')
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '02:34:56.78', 'dec': '-59:53:24.6'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['sn_name'], ['This SN is already registered'])

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

class PhotometryFormTest(TestCase):

    def test_default(self):
        form=PhotometryForm()
        self.assertIn('MJD', form.as_p())

    def test_form_has_placeholders(self):
        form=PhotometryForm()
        self.assertIn('placeholder="Modified Julian Date"', form.as_p())
        self.assertIn('placeholder="One filter at the time, e.g. B"', form.as_p())
        self.assertIn('placeholder="Mag"', form.as_p())

    def test_notes_are_not_required(self):
        form=PhotometryForm(data={'MJD': 54005.0, 'Filter': 'B', 'magnitude': 15.5, 'mag_error': 0.02})
        self.assertTrue(form.is_valid())

    def test_form_saves_data(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        form=PhotometryForm(data={'MJD': 54005.0, 'Filter': 'B', 'magnitude': 15.5, 'mag_error': 0.02})
        self.assertTrue(form.is_valid())
        form.save(sn)
        phot=Photometry.objects.first()
        self.assertEqual(phot.MJD, 54005.0)

class UploadPhotometryFileFormTest(TestCase):

    def test_default(self):
        form=UploadPhotometryFileForm()
        self.assertIn('File', form.as_p())
