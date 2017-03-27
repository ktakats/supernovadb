from .base import FunctionalTest
import time

class LoginTest(FunctionalTest):

    def test_user_can_log_in(self):
        #Joe goes to the SN page
        self.browser.get(self.server_url)

        #The page is asking him to log in
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("Please log in", body)

        #Luckily he already has a password, so he logs in
        self.browser.find_element_by_id("id_email").send_keys("joe@example.com")
        self.browser.find_element_by_id("id_password").send_keys("joepassword\n")

        #After loggin in, he finds himself at his account page
        self.browser.find_element_by_link_text("Hola, Joe")
        self.fail()
