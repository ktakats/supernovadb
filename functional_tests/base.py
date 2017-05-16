from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY
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
        self.browser.implicitly_wait(20)

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()

    #Helper functions
    def create_pre_authenticated_session(self, email, password, first_name):
        user=User.objects.create_user(email=email, password=password, first_name=first_name)
        session=SessionStore()
        session[SESSION_KEY]=user.pk
        session[BACKEND_SESSION_KEY]=settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url)
        self.browser.find_element_by_id("id_email").send_keys(email)
        self.browser.find_element_by_id("id_password").send_keys(password + "\n")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))



    def go_to_page_and_log_in(self):
        self.browser.get(self.server_url)
        User.objects.create_user(email="joe@example.com", password="joepassword", first_name="Joe")
        self.browser.find_element_by_id("id_email").send_keys("joe@example.com")
        self.browser.find_element_by_id("id_password").send_keys("joepassword\n")

    def second_user(self):
        User.objects.create_user(email="claudia@example.com", password="claudiapassword", first_name="Claudia")

    def add_new_sn(self, name="SN 1987A", ra='05:35:27.99', dec='-69:16:11.50'):
        self.browser.find_element_by_link_text('My stuff').click()
        self.browser.find_element_by_id('btn_new_sn').click()
        self.browser.find_element_by_id("id_sn_name").send_keys(name)
        self.browser.find_element_by_id("id_ra").send_keys(ra)
        self.browser.find_element_by_id("id_dec").send_keys(dec + '\n')

    def add_new_project(self, title="Joe's type II project", description="Our project to study type IIs", sn="SN 1987A"):
        self.browser.find_element_by_link_text('My stuff').click()
        self.browser.find_element_by_id('btn_new_project').click()
        self.browser.find_element_by_id("id_title").send_keys(title)
        self.browser.find_element_by_id("id_description").send_keys(description)
        self.browser.find_element_by_id("id_sne").send_keys(sn)
        self.browser.find_element_by_id("id_submit").click()
