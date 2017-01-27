from .base import FunctionalTest
from django.contrib.auth.models import User
import time

class NewSNPageTest(FunctionalTest):

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
        #He adds SN 1987A with  05:35:27.99 -69:16:11.50
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')

        #It brings him to the newly created page of the SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 1987A', title)

    def test_user_cannot_submit_blank_form(self):
        #Joe goes to the New SN form and tries to submit a blank form
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Add new SN').click()

        self.browser.find_element_by_id("id_sn_name").send_keys('\n')
        self.assertIn('Add a new SN', self.browser.find_element_by_tag_name('body').text)

        #So he adds an SN name, but tries to submit without coordinates
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A\n')
        self.assertIn('Add a new SN', self.browser.find_element_by_tag_name('body').text)

    def test_user_cannot_add_duplicate_sn(self):
        #Joe goes to the New SN form and adds an SN
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Add new SN').click()
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')

        #Then he goes away. Next day he forgets that he added this SN and tries again, but gets an error telling him this SN is already in the database
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Add new SN').click()
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')
        error=self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, 'This SN is already registered')
