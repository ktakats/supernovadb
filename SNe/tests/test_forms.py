from django.test import TestCase
from SNe.forms import NewSNForm, AddCoIForm, NewProjectForm
from SNe.models import SN
from django.contrib import auth

User=auth.get_user_model()

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
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '01:34:56.78', 'dec': '-69:53:24.6'})
        self.assertTrue(form.is_valid())
        form.save(user)
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
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2999A', pi=user)
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '02:34:56.78', 'dec': '-59:53:24.6', 'pi': user})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['sn_name'], ['This SN is already registered'])


class AddCoIFormTest(TestCase):

    def test_cant_add_coi_if_hes_pi(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2999A', pi=user)
        form=AddCoIForm(data={'coinvestigators': user.id}, instance=sn)
        self.assertFalse(form.is_valid())

    def test_cant_add_coi_twice(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2999A', pi=pi)
        user=User.objects.create_user(email='coi@test.com', password="blabla", first_name="Coi")
        sn.coinvestigators.add(user)
        sn.save()
        form=AddCoIForm(data={'coinvestigators': user.id}, instance=sn)
        self.assertFalse(form.is_valid())

class NewProjectFormTest(TestCase):

    def test_default(self):
        form=NewProjectForm()
        self.assertIn("id_title", form.as_p())

    def test_title_is_required(self):
        form=NewProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['title'], ["Give a title to your project"])

    def test_cois_exclude_pi(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        form=NewProjectForm(data={'title': 'Bla'}, instance=user)
        self.assertNotIn(user.first_name, form.as_p())

    def test_sne_only_include_pi_sne(self):
        user1=User.objects.create_user(email='test1@test.com', password="bla", first_name="Test1")
        user2=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        user3=User.objects.create_user(email='test3@test.com', password="bla", first_name="Test3")
        sn1=SN.objects.create(sn_name='SN 2999A', pi=user1)
        sn2=SN.objects.create(sn_name='SN 1999A', pi=user2)
        sn2.coinvestigators.add(user1)
        sn2.save()
        sn3=SN.objects.create(sn_name='SN 3999A', pi=user3)
        form=NewProjectForm(data={'title': 'Bla'}, instance=user1)
        self.assertIn(sn1.get_absolute_url(), form.as_p())
        self.assertIn(sn2.get_absolute_url(), form.as_p())
        self.assertNotIn(sn3.get_absolute_url(), form.as_p())
