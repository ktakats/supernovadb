from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from selenium import webdriver
import sys
from django.contrib import auth

User=auth.get_user_model()

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url='http://' + arg.split('=')[1]
                cls.against_staging=True
                return
        super(FunctionalTest, cls).setUpClass()
        cls.against_staging=False
        cls.server_url=cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url==cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        self.browser=webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()

    #Helper functions
    def go_to_page_and_log_in(self):
        self.browser.get(self.server_url)
        User.objects.create_user(username="joe@example.com", password="joepassword", first_name="Joe")
        self.browser.find_element_by_id("id_username").send_keys("joe@example.com")
        self.browser.find_element_by_id("id_password").send_keys("joepassword\n")


    def add_new_sn(self, name="SN 1987A", ra='05:35:27.99', dec='-69:16:11.50'):
        self.browser.find_element_by_link_text('Add a new SN').click()
        self.browser.find_element_by_id("id_sn_name").send_keys(name)
        self.browser.find_element_by_id("id_ra").send_keys(ra)
        self.browser.find_element_by_id("id_dec").send_keys(dec + '\n')
