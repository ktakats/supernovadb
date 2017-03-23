from django.test import TestCase
from SNe.models import SN

class SpectroscopyViewTest(TestCase):

    def test_view_uses_spectroscopy_template(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertTemplateUsed(response, 'spectroscopy.html')

    def test_view_returns_correct_sn_name(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertContains(response, 'SN 2017A')

    def test_view_renders_form(self):
        sn=SN.objects.create(sn_name='SN 2017A', ra=22.625, dec=65.575)
        response=self.client.get('/sn/%d/spectroscopy/' % (sn.id))
        self.assertContains(response, "id_file")
