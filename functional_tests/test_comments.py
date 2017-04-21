from .base import FunctionalTest
from datetime import datetime

class CommentsTest(FunctionalTest):

    def test_sn_comments(self):
        #Joe goes to the SN page, logs in and adds an SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        #He sees an option to add comments to the SN, so he writes something
        self.browser.find_element_by_id("id_comment").send_keys("I added this SN\n")

        #The page refreshes, and he can see his comment, together with his name and the current time
        pub_time=datetime.now()
        comment=self.browser.find_element_by_css_selector(".comments").text
        self.assertIn("Joe", comment)
        self.assertIn("I added this SN", comment)
        self.assertIn(pub_time, comment)
