from astropy import units as u
from astropy.coordinates import SkyCoord
from .base import UnitTests
from SNe.models import SN, Project
from Comments.models import Comment

from django.contrib import auth

User=auth.get_user_model()



def user_login(self):
    user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
    self.client.force_login(user)
    return user

class HomeViewTest(UnitTests):

    def test_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'SNe/home.html')

    def test_user_can_log_in(self):
        User.objects.create_user(email="test@test.com", password="bla", first_name="Test")
        response=self.client.post('/', data={'email': 'test@test.com', 'password': 'bla'})
        user=auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())

    def test_login_redirects_to_my_stuff(self):
        User.objects.create_user(email="test@test.com", password="bla", first_name="Test")
        response=self.client.post('/', data={'email': 'test@test.com', 'password': 'bla'})
        user=auth.get_user(self.client)
        self.assertRedirects(response, '/my_stuff/')

    def test_view_has_link_to_password_reset(self):
        response=self.client.get('/')
        self.assertContains(response, 'I forgot my password')


class SNViewTest(UnitTests):

    def test_view_uses_sn_template(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertTemplateUsed(response, 'SNe/sn.html')

    def test_view_shows_the_name_and_coordinates_of_sn(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'SN 2017A')
        self.assertContains(response, '01:30:30.000')
        self.assertContains(response, '65:34:30.00')

    def test_view_has_link_to_obslog(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Observations')

    def test_view_has_link_to_photometry(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Photometry')

    def test_view_has_link_to_spectroscopy(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Spectroscopy')

    def test_view_requires_login(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/' % (sn.id))

    def test_view_shows_pi(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, "Test")

    def test_view_shows_cois(self):
        sn=self.login_and_create_new_SN()
        coi=User.objects.create_user(email="bla@bla.com", password="test", first_name="Co-I1")
        sn.coinvestigators.add(coi)
        sn.save
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, "Co-I1")

    def test_view_has_comment_section(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, "id_comment")


class AddNewSNViewTest(UnitTests):

    def test_uses_new_sn_template(self):
        user=user_login(self)
        response=self.client.get('/add_sn/')
        self.assertTemplateUsed(response, 'SNe/new_sn.html')

    def test_new_sn_page_renders_form(self):
        user=user_login(self)
        response=self.client.get('/add_sn/')
        self.assertContains(response, 'id_sn_name')

    def test_form_creates_new_database_entry(self):
        user=user_login(self)
        self.client.post('/add_sn/', data={'sn_name': 'SN 1999A', 'ra': '01:23:45.6', 'dec': '+65:34:27.3', 'pi': user, 'host': 'NGC 1234', 'z': 0.02})
        sn=SN.objects.first()
        c=SkyCoord('01:23:45.6', '+65:34:27.3', unit=(u.hourangle, u.deg))
        self.assertEqual(sn.sn_name, 'SN 1999A')
        self.assertEqual('%.2f' % (sn.ra), '%.2f' %  (c.ra.deg))
        self.assertEqual('%.2f' % (sn.dec), '%.2f' % (c.dec.deg))
        self.assertEqual(sn.z, 0.02)

    def test_form_submission_redirects_to_sn_page(self):
        user=user_login(self)
        response=self.client.post('/add_sn/', data={'sn_name': 'SN 1999A', 'ra': '01:23:45.6', 'dec': '+65:34:27.3', 'pi': user})
        sn=SN.objects.first()
        self.assertRedirects(response, '/sn/%d/' % (sn.id))

    def test_view_requires_login(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        response=self.client.post('/add_sn/', data={'sn_name': 'SN 1999A', 'ra': '01:23:45.6', 'dec': '+65:34:27.3', 'pi': user})
        self.assertRedirects(response, '/?next=/add_sn/')
        self.assertEqual(SN.objects.count(), 0)

class EditSNViewTest(UnitTests):

    def test_view_uses_editsn_template(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/edit/' % (sn.id))
        self.assertTemplateUsed(response, 'SNe/edit_sn.html')

    def test_view_renders_form(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/edit/' % (sn.id))
        self.assertContains(response, "id_host")

    def test_redirects_after_submission(self):
        sn=self.login_and_create_new_SN()
        response=self.client.post('/sn/%d/edit/' % (sn.id), data={'sn_name': sn.sn_name,'ra': '01:23:45.6', 'dec': '+65:34:27.3',  'host': 'NGC 123'})
        self.assertRedirects(response, '/sn/%d/' % (sn.id))

    def test_view_requires_login(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        response=self.client.get('/sn/%d/edit/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/edit/' % (sn.id))

class MyStuffViewTest(UnitTests):

    def test_view_uses_mysn_template(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/my_stuff/')
        self.assertTemplateUsed(response, 'SNe/my_stuff.html')

    def test_view_lists_sne(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/my_stuff/')
        self.assertIn(sn,response.context['sne'])

    def test_view_lists_projects(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Bla", pi=User.objects.first())
        project.sne.add(sn)
        response=self.client.get('/my_stuff/')
        self.assertIn(project, response.context['projects'])

    def test_view_only_shows_related_projects(self):
        sn=self.login_and_create_new_SN()
        project1=Project.objects.create(title="Bla")
        project2=Project.objects.create(title="Bla", pi=User.objects.first())
        project1.sne.add(sn)
        response=self.client.get('/my_stuff/')
        self.assertNotIn(project1, response.context['projects'])
        self.assertIn(project2, response.context['projects'])

    def test_can_see_sne_as_coI(self):
        sn=self.login_and_create_new_SN()
        self.client.logout()
        user=User.objects.create_user(email='test2@test.com', password="bla", first_name="Test2")
        sn.coinvestigators.add(user)
        sn.save()
        self.client.force_login(user)
        response=self.client.get('/my_stuff/')
        self.assertIn(sn, response.context['sne'])

class AddNewProjectViewTest(UnitTests):

    def test_view_uses_new_project_template(self):
        user=user_login(self)
        response=self.client.get('/add_project/')
        self.assertTemplateUsed(response, 'SNe/new_project.html')

    def test_view_renders_form(self):
        user=user_login(self)
        response=self.client.get('/add_project/')
        self.assertContains(response, 'id_title')

    def test_view_requires_login(self):
        response=self.client.get('/add_project/')
        self.assertRedirects(response, '/?next=/add_project/')

    def test_submitting_form_saves_project(self):
        sn=self.login_and_create_new_SN()
        response=self.client.post('/add_project/', data={'title': "Bla", 'description': "bla bla", 'sne': sn.id}, user=User.objects.first())
        project=Project.objects.first()
        self.assertEqual(project.title, "Bla")

    def test_form_submission_redirects_to_project_page(self):
        sn=self.login_and_create_new_SN()
        response=self.client.post('/add_project/', data={'title': "Bla", 'description': "bla bla", 'sne': sn.id}, user=User.objects.first())
        project=Project.objects.first()
        self.assertRedirects(response, '/projects/%d/' % (project.id))

class ProjectViewTest(UnitTests):

    def test_view_renders_template_and_shows_correct_project(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Bla")
        response=self.client.get('/projects/%d/' % (project.id))
        self.assertTemplateUsed(response, 'SNe/project.html')

    def test_view_requires_login(self):
        project=Project.objects.create(title="Bla")
        response=self.client.get('/projects/%d/' % (project.id))
        self.assertRedirects(response, '/?next=/projects/%d/' % (project.id))

class EditProjectViewTest(UnitTests):

    def test_view_renders_template(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Bla", pi=User.objects.first())
        response=self.client.get('/projects/%d/edit/' % (project.id))
        self.assertTemplateUsed(response, 'SNe/edit_project.html')

    def test_view_renders_form(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Bla", description="blabla", pi=User.objects.first())
        response=self.client.get('/projects/%d/edit/' % (project.id))
        self.assertContains(response, 'id_description')

    def test_form_contains_project_details(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Bla", description="blabla", pi=User.objects.first())
        response=self.client.get('/projects/%d/edit/' % (project.id))
        self.assertContains(response, 'value="Bla"')

    def test_form_redirects_after_submission(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Bla", description="blabla", pi=User.objects.first())
        response=self.client.post('/projects/%d/edit/' % (project.id), data={'title': "Blabla", 'description': "blabla"})
        self.assertRedirects(response, '/projects/%d/' % (project.id))

class SNCommentsViewTest(UnitTests):

    def test_view_shows_comment_form(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'id_text')

    def test_view_shows_comments(self):
        sn=self.login_and_create_new_SN()
        user=User.objects.first()
        comment=Comment.objects.create(text="Bla", author=user)
        sn.comments.add(comment)
        sn.save()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, "Bla")

    def test_can_submit_form_then_redirect(self):
        sn=self.login_and_create_new_SN()
        response=self.client.post('/sn/%d/' % (sn.id), data={'text': "Testtest test"})
        self.assertEqual(sn.comments.count(), 1)
        self.assertRedirects(response, '/sn/%d/' % (sn.id))

class ProjectCommentsViewTest(UnitTests):

    def test_view_shows_comment_form(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Title" )
        response=self.client.get('/projects/%d/' % (project.id))
        self.assertContains(response, 'id_text')

    def test_view_shows_comments(self):
        sn=self.login_and_create_new_SN()
        user=User.objects.first()
        project=Project.objects.create(title="Title" )
        comment=Comment.objects.create(text="Bla", author=user)
        project.comments.add(comment)
        project.save()
        response=self.client.get('/projects/%d/' % (project.id))
        self.assertContains(response, "Bla")

    def test_can_submit_form_then_redirect(self):
        sn=self.login_and_create_new_SN()
        project=Project.objects.create(title="Title" )
        response=self.client.post('/projects/%d/' % (project.id), data={'text': "Testtest test"})
        self.assertEqual(project.comments.count(), 1)
        self.assertRedirects(response, '/projects/%d/' % (project.id))
