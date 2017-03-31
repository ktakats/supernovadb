from astropy import units as u
from astropy.coordinates import SkyCoord
from .base import UnitTests
from SNe.models import SN

from django.contrib import auth

User=auth.get_user_model()



def user_login(self):
    user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
    self.client.force_login(user)
    return user

class HomeViewTest(UnitTests):

    def test_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_user_can_log_in(self):
        User.objects.create_user(email="test@test.com", password="bla", first_name="Test")
        response=self.client.post('/', data={'email': 'test@test.com', 'password': 'bla'})
        user=auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())


class SNViewTest(UnitTests):

    def test_view_uses_sn_template(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        self.client.force_login(user)
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertTemplateUsed(response, 'sn.html')

    def test_view_shows_the_name_and_coordinates_of_sn(self):
        sn=self.login_and_create_new_SN()
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'SN 2017A')
        self.assertContains(response, 'RA=01:30:30.000')
        self.assertContains(response, 'Dec=65:34:30.00')

    def test_view_has_link_to_obslog(self):
        sn=self.login_and_create_new_SN(self)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Observation log')

    def test_view_has_link_to_photometry(self):
        sn=self.login_and_create_new_SN(self)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Photometry')

    def test_view_has_link_to_spectroscopy(self):
        sn=self.login_and_create_new_SN(self)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertContains(response, 'Spectroscopy')

    def test_view_requires_login(self):
        user=User.objects.create_user(email='test@test.com', password="bla", first_name="Test")
        sn=SN.objects.create(sn_name='SN 2017A', pi=user)
        response=self.client.get('/sn/%d/' % (sn.id))
        self.assertRedirects(response, '/?next=/sn/%d/' % (sn.id))


class AddNewSNViewTest(UnitTests):

    def test_uses_new_sn_template(self):
        user=user_login(self)
        response=self.client.get('/add_sn/')
        self.assertTemplateUsed(response, 'new_sn.html')

    def test_new_sn_page_renders_form(self):
        user=user_login(self)
        response=self.client.get('/add_sn/')
        self.assertContains(response, 'id_sn_name')

    def test_form_creates_new_database_entry(self):
        user=user_login(self)
        self.client.post('/add_sn/', data={'sn_name': 'SN 1999A', 'ra': '01:23:45.6', 'dec': '+65:34:27.3', 'pi': user})
        sn=SN.objects.first()
        c=SkyCoord('01:23:45.6', '+65:34:27.3', unit=(u.hourangle, u.deg))
        self.assertEqual(sn.sn_name, 'SN 1999A')
        self.assertEqual('%.2f' % (sn.ra), '%.2f' %  (c.ra.deg))
        self.assertEqual('%.2f' % (sn.dec), '%.2f' % (c.dec.deg))

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

class MySNeViewTest(UnitTests):

    def test_view_uses_mysn_template(self):
        sn=self.login_and_create_new_SN(self)
        response=self.client.get('/my_sne/')
        self.assertTemplateUsed(response, 'my_sne.html')

    def test_view_lists_sne(self):
        sn=self.login_and_create_new_SN(self)
        response=self.client.get('/my_sne/')
        self.assertIn(sn,response.context['sne'])
