from .base import FunctionalTest
from django.contrib.auth.models import User

class SnPageTest(FunctionalTest):

    def test_user_can_add_SN_and_access_its_page(self):
        #There's a new app for SNe! Joe goes and checks it out
        user=User.objects.create()
        self.browser.get(self.server_url)

        #Sees that it's really about SNe!
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('Supernovae', title)

        #Finds a field where he can add a new SN. He adds SN 2017A
        self.browser.find_element_by_id('id_new_sn').send_keys('SN 2017A\n')

        #It brings him to the newly created page of the SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 2017A', title)
