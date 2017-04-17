from .base import FunctionalTest

class MySruffTest(FunctionalTest):

    def test_user_can_have_all_their_SNe_in_a_page(self):
        #Joe goes to the SN page, and adds 2 new SNe and  new project
        self.go_to_page_and_log_in()
        self.add_new_sn()
        self.add_new_sn(name='SN 1988A',ra='12:37:43.58', dec='11:48:19.69')
        self.add_new_project()
        #time.sleep(5)
        #He goes to see the list of his SNe
        self.browser.find_element_by_link_text("My stuff").click()

        #Here both if his SNe and his project are listed
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn("SN 1987A", body)
        self.assertIn("SN 1988A", body)
        self.assertIn("Joe's type II project", body)

        #Clicking on an SN takes him to the SN's page
        self.browser.find_element_by_link_text("SN 1987A").click()
        title=self.browser.find_element_by_tag_name('h1').text

        self.assertEqual(title, "SN 1987A")
        self.browser.back()

        #Clicking on the project takes him to the project's page
        self.browser.find_element_by_link_text("Joe's type II project").click()
        title=self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(title, "Joe's type II project")
