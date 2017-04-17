from .base import FunctionalTest
import time

from django.contrib import auth

User=auth.get_user_model()

class LoginTest(FunctionalTest):

    def test_user_can_log_in(self):
        #Joe goes to the SN page
        self.browser.get(self.server_url)

        #The page is asking him to log in
        User.objects.create_user(email="joe@example.com", password="joepassword", first_name="Joe")
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("Please log in", body)

        #He tries to log in, but puts a wrong password so gets an error
        self.browser.find_element_by_id("id_email").send_keys("joe@example.com")
        self.browser.find_element_by_id("id_password").send_keys("joe\n")
        error=self.browser.find_element_by_tag_name('body').text

        self.assertIn("Login is invalid. Please try again.", error)
        time.sleep(5)
        #Luckily he remembers his password, so he logs in

        self.browser.find_element_by_id("id_password").send_keys("joepassword\n")

        #After loggin in, he finds himself at his account page
        self.browser.find_element_by_link_text("Logout")
        self.assertEqual("Joe's stuff", self.browser.find_element_by_tag_name("h1").text)

    def test_user_has_to_be_logged_in(self):
        #Joe tries to go to the add SN page
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text("My stuff").click()


        #But since he's not logged in, he's redirected to to the home
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("Please log in", body)
