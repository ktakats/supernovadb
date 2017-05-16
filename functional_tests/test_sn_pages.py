from .base import FunctionalTest
import time

class NewSNPageTest(FunctionalTest):

    def test_user_can_add_SN_and_access_its_page(self):
        #There's a new app for SNe! Joe goes and checks it out
        self.second_user()
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
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50')
        self.browser.find_element_by_id("id_sntype").send_keys('II-P')
        self.browser.find_element_by_id("id_host").send_keys('NGC 1234')
        self.browser.find_element_by_id("id_coinvestigators").send_keys("Claudia")
        self.browser.find_element_by_id("id_z").send_keys("0.01\n")

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
        time.sleep(10)
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

        #The SN he's done with can be archived
        self.browser.find_element_by_css_selector(".fa-archive").click()
        time.sleep(2)
        self.browser.find_element_by_id("id_confirmbutton").click()
        # after archiving the SN is not visible on any pages
        self.browser.find_element_by_link_text("My stuff").click()
        body=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('SN 1987A', body)

        self.browser.find_element_by_id('btn_new_sn').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('SN 1987A', body)

    def test_user_can_see_projects_associated_with_sn(self):
        # There's a new app for SNe! Joe goes and checks it out
        self.second_user()
        self.go_to_page_and_log_in()
        #he creates an sn
        self.add_new_sn()
        #and a project
        self.add_new_project()
        #he goes to the SN's page and sees the project there
        self.browser.find_element_by_link_text("My stuff").click()
        self.browser.find_element_by_link_text("SN 1987A").click()
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn("Joe's type II project", body)

        # clicking on the project takes the user to the project page
        self.browser.find_element_by_link_text("Joe's type II project").click()
        h1=self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(h1, "Joe's type II project")

class EditSNDataTest(FunctionalTest):

    def test_user_can_edit_sn_data(self):
        #Joe goes to the SN site and adds an SN
        self.second_user()
        self.go_to_page_and_log_in()
        self.add_new_sn()

        #Now he's at the page of this new SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 1987A', title)

        #He needs to add the host galaxy data
        #He finds the edit button
        self.browser.find_element_by_css_selector(".fa-pencil").click()
        #It leads him to the edit page of the SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertEqual(title, "Edit SN")
        #He adds the new data
        self.browser.find_element_by_id("id_z").send_keys("0.01")
        self.browser.find_element_by_id("id_host").send_keys("LMC")
        self.browser.find_element_by_id("id_coinvestigators").send_keys("Claudia")
        self.browser.find_element_by_id("id_ra").clear()
        self.browser.find_element_by_id("id_ra").send_keys("05:35:28.99\n")
        ##Submittin the form takes him back to the SN page
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn('SN 1987A', title)
        #Here he can see the new data he just entered
        body=self.browser.find_element_by_css_selector('body').text
        self.assertIn("RA: 05:35:28.99", body)
        self.assertIn("Claudia", body)
        self.assertIn("Host: LMC", body)
        self.assertIn("z: 0.01", body)

class EditProjectDataTest(FunctionalTest):

    def test_user_can_edit_project_data(self):
        #Joe goes to the SN site and adds an SN
        self.second_user()
        self.go_to_page_and_log_in()
        self.add_new_sn()
        self.add_new_sn(name="SN 1988A", ra='06:35:27.99', dec='-59:16:11.50')

        #He creates a project and adds the sn
        self.add_new_project()

        #He needs to edit the project details
        #He finds the edit button
        self.browser.find_element_by_css_selector(".fa-pencil").click()
        #It leads him to the edit page of the SN
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertEqual(title, "Edit project")
        time.sleep(10)
        #He adds the new data
        self.browser.find_element_by_id("id_description").clear()
        self.browser.find_element_by_id("id_description").send_keys("Our project to study type II-Ps")
        self.browser.find_element_by_id("id_sne").send_keys("SN 1988A")
        self.browser.find_element_by_id("id_coinvestigators").send_keys("Claudia\n")
        time.sleep(10)
        ##Submittin the form takes him back to the SN page
        title=self.browser.find_element_by_css_selector('h1').text
        self.assertIn("Joe's type II project", title)
        #Here he can see the new data he just entered
        body=self.browser.find_element_by_css_selector('body').text
        self.assertIn("Claudia", body)
        self.assertIn("Our project to study type II-Ps", body)
        self.assertIn("SN 1988A", body)

        #Now he's done with the project and archives it
        self.browser.find_element_by_css_selector('.fa-archive').click()
        time.sleep(2)
        self.browser.find_element_by_id("id_confirmbutton").click()
        #Now the project is not in the My stuff page
        self.browser.find_element_by_link_text('My stuff').click()
        body=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Joe's type II project", body)
        #And can't be added to SNe either
        self.browser.find_element_by_id('btn_new_sn').click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Joe's type II project", body)




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
        time.sleep(10)
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
