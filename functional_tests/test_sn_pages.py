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

        #Finds a button where he can add a new SN. He clicks it
        self.browser.find_element_by_link_text('Add new SN').click()

        #There's a form here to add the name and the coordinates of the new SN.
        #First he tries to submit an empty form, which is not accepted

        #Then he makes a mistake with the coordinates.

        #He adds SN 1987A with  05:35:27.99 -69:16:11.50, which is correct form


        self.browser.find_element_by_id("id_new_sn").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_coord").send_keys('05:35:27.99 -69:16:11.50\n')

        #It brings him to the newly created page of the SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 2017A', title)
