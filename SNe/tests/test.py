from django.test import TestCase
from SNe.models import SN

class HomeViewTest(TestCase):

    def test_uses_home_template(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_has_input_for_new_sn(self):
        response=self.client.get('/')
        self.assertContains(response, 'id_new_sn')

    def test_input_new_sn_redirects_to_sn_page(self):
        response=self.client.post('/add_sn/', data={'new_sn': 'SN 2000A'})
        sn=SN.objects.get(sn_name='SN 2000A')
        self.assertRedirects(response, '/%d/' % (sn.id))


class SNViewTest(TestCase):

    def test_view_uses_sn_template(self):
        sn=SN.objects.create(sn_name='SN 2017A')
        response=self.client.get('/%d/' % (sn.id))
        self.assertTemplateUsed(response, 'sn.html')
