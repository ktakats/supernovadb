from django.test import TestCase
from SNe.forms import NewSNForm
from SNe.models import SN

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

    #test for digit limits!!!
