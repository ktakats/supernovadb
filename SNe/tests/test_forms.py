from django.test import TestCase
from SNe.forms import NewSNForm, NewProjectForm
from SNe.models import SN, Project
from django.contrib import auth

User=auth.get_user_model()

class NewSNFormTest(TestCase):

    def test_form_has_placeholders(self):
        form=NewSNForm()
        self.assertIn('00:00:00.00', form.as_p())
        self.assertIn('e.g.: 55060.0 (discovery)', form.as_p())

    def test_form_validation_for_blank_items(self):
        form=NewSNForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['sn_name'], ['You need to provide the name of the SN'])

    def test_form_validation_for_coords(self):
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '01:34:56.78', 'dec': '-69:53:24.6'})
        self.assertTrue(form.is_valid())

    def test_coords_are_saved_to_database(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        form=NewSNForm(user=user,data={'sn_name': 'SN 2999A', 'ra': '01:34:56.78', 'dec': '-69:53:24.6'})
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
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '25:45:56.78', 'dec': '-69:53:-24.0'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['ra'], ['Invalid coordinate value'])
        self.assertEqual(form.errors['dec'], ['Incorrect coordinate format'])

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

    def test_can_add_cois(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        coi=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '02:34:56.78', 'dec': '-59:53:24.6', 'coinvestigators': [coi.id]})
        self.assertTrue(form.is_valid())
        form.save(user)
        sn=SN.objects.first()
        self.assertEqual(sn.coinvestigators.first(), coi)

    def test_can_add_projects(self):
        user = User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        project1=Project.objects.create(title="Bla", pi=user)
        project2=Project.objects.create(title="Bla2", pi=user)
        form=NewSNForm(data={'sn_name': 'SN 2999A', 'ra': '02:34:56.78', 'dec': '-59:53:24.6', 'projects': [project1.id, project2.id]}, user=user)
        self.assertTrue(form.is_valid())
        form.save(user)
        sn=SN.objects.first()
        self.assertEqual(project1.sne.first(), sn)
        self.assertEqual(project2.sne.first(), sn)

    def test_only_can_add_projects_where_user_is_investigator(self):
        user1=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        user2=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        project1 = Project.objects.create(title="Bla", pi=user1)
        project2 = Project.objects.create(title="Bla2", pi=user2)
        project3=Project.objects.create(title="Bla3", pi=user2)
        project3.coinvestigators.add(user1)
        project3.save()
        form=NewSNForm(user=user1)
        self.assertIn(project1.title, form.as_p())
        self.assertNotIn(project2.title, form.as_p())
        self.assertIn(project3.title, form.as_p())

    def test_only_can_add_project_that_are_not_archived(self):
        user = User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        project1 = Project.objects.create(title="Bla", pi=user)
        project2 = Project.objects.create(title="Bla2", pi=user, archived=True)
        form=NewSNForm(user=user)
        self.assertIn(project1.title, form.as_p())
        self.assertNotIn(project2.title, form.as_p())

    def test_edit_sn_details(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2999A', pi=user, ra=22.625, dec=65.575)
        form=NewSNForm(instance=sn, initial={'ra': sn.ra, 'dec': sn.dec})
        self.assertIn('value="22.625"',form.as_p())


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

        form=NewProjectForm(data={'title': 'Bla'}, user=user)
        self.assertNotIn(user.first_name, form.as_p())

    def test_new_project_offers_sn(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        user2=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        sn1=SN.objects.create(sn_name='SN 2999A', pi=user)
        form=NewProjectForm(user=user)
        self.assertIn(sn1.sn_name, form.as_p())
        self.assertIn(user2.first_name, form.as_p())

    def test_sne_only_include_pi_sne(self):
        user1=User.objects.create_user(email='test1@test.com', password="bla", first_name="Test1")
        user2=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        user3=User.objects.create_user(email='test3@test.com', password="bla", first_name="Test3")
        sn1=SN.objects.create(sn_name='SN 2999A', pi=user1)
        sn2=SN.objects.create(sn_name='SN 1999A', pi=user2)
        sn2.coinvestigators.add(user1)
        sn2.save()
        sn3=SN.objects.create(sn_name='SN 3999A', pi=user3)
        form=NewProjectForm(data={'title': 'Bla'}, user=user1)
        self.assertIn(sn1.sn_name, form.as_p())
        self.assertIn(sn2.sn_name, form.as_p())
        self.assertNotIn(sn3.sn_name, form.as_p())

    def test_sne_doesnot_include_archived_sne(self):
        user = User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn1 = SN.objects.create(sn_name='SN 2999A', pi=user)
        sn2 = SN.objects.create(sn_name='SN 1999A', pi=user, archived=True)
        form=NewProjectForm(user=user)
        self.assertNotIn(sn2.sn_name, form.as_p())

    def test_save_form(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        user2=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        sn1=SN.objects.create(sn_name='SN 2999A', pi=user)
        sn2=SN.objects.create(sn_name='SN 1999A', pi=user)
        form=NewProjectForm(data={'title': "Bla", 'description': "bla bla", 'sne': [sn1.id, sn2.id], 'coinvestigators': [user2.id]}, user=user)
        self.assertTrue(form.is_valid())
        form.save(user)
        p=Project.objects.first()
        self.assertEqual(p.title, "Bla")
        self.assertEqual(p.pi, user)
        self.assertIn(sn2, p.sne.all())
        self.assertIn(user2, p.coinvestigators.all())

    def test_cois_become_cois_of_SNe(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn1=SN.objects.create(sn_name='SN 2999A', pi=pi)
        user2=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        form=NewProjectForm(data={'title': "Bla", 'description': "bla bla", 'sne': [sn1.id], 'coinvestigators': [user2.id]}, user=pi)
        self.assertTrue(form.is_valid())
        form.save(pi)
        self.assertIn(user2, sn1.coinvestigators.all())

    def test_can_edit_project_details(self):
        pi=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        project=Project.objects.create(title="Bla", description="blabla", pi=pi)
        form=NewProjectForm(data={'title': "Blabla", 'description':"bla"}, instance=project)
        self.assertTrue(form.is_valid())
        form.save(pi, project.id)
        self.assertEqual(Project.objects.count(),1)
        self.assertEqual(project.title, "Blabla")

    def test_edit_form_exludes_existing_cois_and_sne(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        user2=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        user3=User.objects.create_user(email='test3@test.com', password="bla", first_name="Test3")
        sn1=SN.objects.create(sn_name='SN 2999A', pi=user)
        sn2=SN.objects.create(sn_name='SN 1999A', pi=user2)
        project=Project.objects.create(title="Bla", description="blabla", pi=user)
        project.coinvestigators.add(user2)
        project.sne.add(sn1)
        project.save()
        self.assertEqual(project.sne.count(),1)
        self.assertEqual(project.coinvestigators.count(),1)
        form=NewProjectForm(instance=project)
        self.assertNotIn(user2.first_name, form.as_p())
        self.assertNotIn(sn1.sn_name,form.as_p())
        self.assertIn(user3.first_name, form.as_p())
        self.assertIn(sn2.sn_name,form.as_p())
