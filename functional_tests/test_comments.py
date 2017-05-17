from .base import FunctionalTest
from datetime import datetime
import time

class CommentsTest(FunctionalTest):

    def test_sn_and_project_comments(self):
        #Joe goes to the SN page, logs in and adds an SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        #He sees an option to add comments to the SN, so he writes something
        self.browser.find_element_by_id("id_text").send_keys("I added this SN")
        self.browser.find_element_by_id("id_submitcomment").click()

        #The page refreshes, and he can see his comment, together with his name and the current time
        pub_time=datetime.now()
        comment=self.browser.find_element_by_css_selector(".comments").text
        self.assertIn("Joe", comment)
        self.assertIn("I added this SN", comment)
        self.assertIn("2017", comment)

        #He adds a project, and notices he has the same option here too
        self.add_new_project()
        self.browser.find_element_by_id("id_text").send_keys("I added this project")
        self.browser.find_element_by_id("id_submitcomment").click()

        comment=self.browser.find_element_by_css_selector(".comments").text
        self.assertIn("Joe", comment)
        self.assertIn("I added this project", comment)
        self.assertIn("2017", comment)
