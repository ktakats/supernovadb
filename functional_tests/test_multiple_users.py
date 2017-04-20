from selenium import webdriver
from .base import FunctionalTest
import time

def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SNSharingTest(FunctionalTest):

    def test_coI_can_see_SNe(self):
        #Joe and Claudia are both logged in users

        self.create_pre_authenticated_session("joe@example.com", "joepassword", "Joe")
        joe_browser=self.browser
        self.addCleanup(lambda: quit_if_possible(joe_browser))

        claudia_browser=webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser=claudia_browser
        self.create_pre_authenticated_session('claudia@example.com', "claudiapassword", "Claudia")
        self.addCleanup(lambda: quit_if_possible(claudia_browser))

        #Joe goes to a page, adds an SN
        self.browser=joe_browser
        self.browser.get(self.server_url)
        self.add_new_sn()


        #He adds Claudia as Co-I
        self.browser.find_element_by_css_selector(".fa-pencil").click()
        self.browser.find_element_by_id("id_coinvestigators").send_keys("Claudia\n")

        #Now Claudia can see and edit the SN and its data
        self.browser=claudia_browser
        self.browser.get(self.server_url+ "/my_stuff/")
        self.assertIn("SN 1987A", self.browser.find_element_by_tag_name('body').text)
