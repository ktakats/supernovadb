from .base import FunctionalTest
import time

class NewSNPageTest(FunctionalTest):

    def test_user_can_add_SN_and_access_its_page(self):
        #There's a new app for SNe! Joe goes and checks it out
        self.go_to_page_and_log_in()

        #Sees that it's really about SNe!
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('Supernova', title)

        #Finds a button where he can add a new SN. He clicks it
        self.browser.find_element_by_link_text('Add a new SN').click()

        #There's a form here to add the name and the coordinates of the new SN.
        #He adds SN 1987A with  05:35:27.99 -69:16:11.50
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')

        #It brings him to the newly created page of the SN, that shows the coordinates too
        title=self.browser.find_element_by_css_selector('h1').text
        coords=self.browser.find_element_by_css_selector('.coordinates').text
        self.assertIn('SN 1987A', title)
        self.assertIn('05:35:27.99', coords)

    def test_user_cannot_submit_blank_form(self):
        #Joe goes to the New SN form and tries to submit a blank form
        self.go_to_page_and_log_in()
        self.browser.find_element_by_link_text('Add a new SN').click()

        self.browser.find_element_by_id("id_sn_name").send_keys('\n')
        self.assertIn('Add a new SN', self.browser.find_element_by_tag_name('body').text)

        #So he adds an SN name, but tries to submit without coordinates
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A\n')
        self.assertIn('Add a new SN', self.browser.find_element_by_tag_name('body').text)

    def test_user_cannot_add_duplicate_sn(self):
        #Joe goes to the New SN form and adds an SN
        self.go_to_page_and_log_in()
        self.add_new_sn(name='SN 1987A', ra='05:35:27.99', dec='-69:16:11.50')

        #Then he goes away. Next day he forgets that he added this SN and tries again, but gets an error telling him this SN is already in the database
        self.browser.get(self.server_url)
        self.add_new_sn(name='SN 1987A', ra='05:35:27.99', dec='-69:16:11.50')
        error=self.browser.find_element_by_css_selector('.errorlist')
        self.assertEqual(error.text, 'This SN is already registered')

class MySneTest(FunctionalTest):

    def test_user_can_have_all_their_SNe_in_a_page(self):
        #Joe goes to the SN page, and adds 2 new SNe
        self.go_to_page_and_log_in()
        self.add_new_sn()
        self.add_new_sn(name='SN 1988A',ra='12:37:43.58', dec='11:48:19.69')
        time.sleep(5)
        #He goes to see the list of his SNe
        self.browser.find_element_by_link_text("My SNe").click()
        time.sleep(5)
        #Here both if his SNe are listed
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn("SN 1987A", body)
        self.assertIn("SN 1988A", body)

        #Clicking on an SN takes him to the SN's page
        self.browser.find_element_by_link_text("SN 1987A").click()
        title=self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(title, "SN 1987A")
