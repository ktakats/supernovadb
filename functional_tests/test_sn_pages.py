from .base import FunctionalTest
import time

class NewSNPageTest(FunctionalTest):

    def test_user_can_add_SN_and_access_its_page(self):
        #There's a new app for SNe! Joe goes and checks it out
        self.go_to_page_and_log_in()
        #Sees that it's really about SNe!
        title=self.browser.find_element_by_css_selector('h1').text
        #self.assertIn('Supernova', title)
        #Finds a button where he can add a new SN. He clicks it
        self.browser.find_element_by_id('btn_new_sn').click()

        #There's a form here to add the name and the coordinates of the new SN.
        #He adds SN 1987A with  05:35:27.99 -69:16:11.50
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')

        #It brings him to the newly created page of the SN, that shows the coordinates too
        title=self.browser.find_element_by_css_selector('h1').text
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('SN 1987A', title)
        self.assertIn('05:35:27.99', body)

    def test_user_cannot_submit_blank_form(self):
        #Joe goes to the New SN form and tries to submit a blank form
        self.go_to_page_and_log_in()
        self.browser.find_element_by_id('btn_new_sn').click()

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

class SNPageTest(FunctionalTest):

    def test_SN_page_functions(self):
        #Joe goes to the SN site and adds an SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        #Now he's at the page of this new SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 1987A', title)

        #There are links to the Observation Logs
        self.browser.find_element_by_link_text("Observations").click()
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "SN 1987A")
        self.browser.back()

        #to the photometry page
        self.browser.find_element_by_link_text("Photometry").click()
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "SN 1987A")
        self.browser.back()
        #and to the spectroscopy page
        self.browser.find_element_by_link_text("Spectroscopy").click()
        self.assertEqual(self.browser.find_element_by_tag_name("h1").text, "SN 1987A")
        self.browser.back()

    def test_SN_page_PI_and_coIs(self):
        #Joe goes to the SN site and adds an SN
        self.second_user()
        self.go_to_page_and_log_in()
        self.add_new_sn()

        #Now he's at the page of this new SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 1987A', title)

        #He can see that he is the PI of this object
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("PI\nJoe", body)

        #He notices that he can add co-Is, so he adds Claudia
        self.browser.find_element_by_id("id_coinvestigators").send_keys("Claudia")
        self.browser.find_element_by_id("id_addbutton").click()

        #Claudia's name appears in a list of co-Is
        body=self.browser.find_element_by_tag_name("body").text
        time.sleep(5)
        self.assertIn("Co-Is", body)
        self.assertIn("Claudia", body)





class NewProjectTest(FunctionalTest):

    def test_user_can_create_projects(self):
        #Joe goes to the SN page and logs in, add an SN
        self.second_user()
        self.go_to_page_and_log_in()
        self.add_new_sn()

        #He notices that he can now create projects!
        self.browser.find_element_by_link_text("My stuff").click()
        self.browser.find_element_by_id("btn_new_project").click()
        self.browser.find_element_by_id("id_title").send_keys("Joe's type II project")
        self.browser.find_element_by_id("id_description").send_keys("Our project to study type IIs")
        self.browser.find_element_by_id("id_sne").send_keys("SN 1987A")
        self.browser.find_element_by_id("id_coinvestigators").send_keys("claudia")
        self.browser.find_element_by_id("id_submit").click()

        time.sleep(10)
        #It brings him back to the my projects page, where he can see the title of the project
        title=self.browser.find_element_by_tag_name("h1").text
        self.assertEqual(title, "Joe's type II project")

        #Here he can see the SNe that belong to the project and the co-is of the project
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('SN 1987A', body)
        self.assertIn('Claudia', body)
        self.assertIn("Our project to study type IIs", body)

        #Clicking on the SN name takes him to the SN's page
        self.browser.find_element_by_link_text('SN 1987A').click()
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 1987A', title)
