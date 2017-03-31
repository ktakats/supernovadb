from django.test import TestCase
from Photometry.forms import PhotometryForm, UploadPhotometryFileForm
from Photometry.models import Photometry
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()

class PhotometryFormTest(TestCase):

    def test_default(self):
        form=PhotometryForm()
        self.assertIn('MJD', form.as_p())

    def test_form_has_placeholders(self):
        form=PhotometryForm()
        self.assertIn('placeholder="Modified Julian Date"', form.as_p())
        self.assertIn('placeholder="Mag"', form.as_p())

    def test_notes_are_not_required(self):
        form=PhotometryForm(data={'MJD': 54005.0, 'Filter': 'B', 'magnitude': 15.5, 'mag_error': 0.02})
        self.assertTrue(form.is_valid())

    def test_form_saves_data(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        form=PhotometryForm(data={'MJD': 54005.0, 'Filter': 'B', 'magnitude': 15.5, 'mag_error': 0.02})
        self.assertTrue(form.is_valid())
        form.save(sn)
        phot=Photometry.objects.first()
        self.assertEqual(phot.MJD, 54005.0)

    def test_phot_entry_is_updated_when_editing(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575, pi=user)
        phot=Photometry.objects.create(sn=sn, MJD=54005.0, Filter='B', magnitude=16.5, mag_error=0.03)
        form=PhotometryForm(data={'MJD':54005.0, 'Filter':'B', 'magnitude': 15.5, 'mag_error':0.03})
        self.assertTrue(form.is_valid())
        updated_phot=form.save(sn=sn, id=phot.id)
        self.assertEqual(phot.id, updated_phot.id)

class UploadPhotometryFileFormTest(TestCase):

    def test_default(self):
        form=UploadPhotometryFileForm()
        self.assertIn('File', form.as_p())
