from .base import FunctionalTest
import time

class ObsLogTest(FunctionalTest):

    def test_SN_user_can_add_observation_to_obs_log(self):
        #Joe goes to the SN page and adds an SN
        self.browser.get(self.server_url)
        self.add_new_sn()

        #Redirected to the SN's page, Joe notices that here he can keep track of the observations
        self.browser.find_element_by_link_text('Observation log').click()

        #Here he sees a form to submit his observations
        self.browser.find_element_by_id('id_obs_date').send_keys("2017-01-01")
        self.browser.find_element_by_id('id_obs_type').send_keys('S')
        self.browser.find_element_by_id('id_telescope').send_keys("NTT")
        self.browser.find_element_by_id('id_instrument').send_keys("EFOSC2")
        self.browser.find_element_by_id('id_setup').send_keys("GR13")
        self.browser.find_element_by_id('id_notes').send_keys("Trial")
        self.browser.find_element_by_tag_name("button").click()

        #After submitting the form the page refreshes and he sees his input in a table format
        self.browser.find_element_by_tag_name("table")
        telescope=self.browser.find_element_by_css_selector('.telescope')

    def test_user_can_edit_and_delete_observation(self):
        #Joe goes to the SN page and adds an SN
        self.browser.get(self.server_url)
        self.add_new_sn()

        #Redirected to the SN's page, Joe notices that here he can keep track of the observations
        self.browser.find_element_by_link_text('Observation log').click()

        #Here he sees a form to submit his observations
        self.browser.find_element_by_id('id_obs_date').send_keys("2017-01-01")
        self.browser.find_element_by_id('id_obs_type').send_keys('S')
        self.browser.find_element_by_id('id_telescope').send_keys("NTT")
        self.browser.find_element_by_id('id_instrument').send_keys("EFOSC2")
        self.browser.find_element_by_id('id_setup').send_keys("GR13")
        self.browser.find_element_by_id('id_notes').send_keys("Trial")
        self.browser.find_element_by_tag_name("button").click()

        #He made a mistake, and wants to edit the entry
        self.browser.find_element_by_css_selector(".fa-pencil").click()
        setup=self.browser.find_element_by_id('id_setup').get_attribute('value')
        self.assertEqual("GR13", setup)
        self.browser.find_element_by_id('id_setup').send_keys("GR13, GR16")
        self.browser.find_element_by_tag_name("button").click()
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("GR13, GR16", body)


        #He notices that it's all wrong, so wants to delete the observation
        self.browser.find_element_by_css_selector(".fa-trash-o").click()
        #it prompts a pop-up, asking him if he's sure. he says yes
        time.sleep(5)
        self.browser.find_element_by_id("id_deletebutton").click()
        #Now the observation is deleted.
        body=self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("NTT", body)

    def test_user_can_add_new_entry_after_editing(self):
        #Joe goes to the SN page and adds an SN
        self.browser.get(self.server_url)
        self.add_new_sn()

        #Redirected to the SN's page, Joe notices that here he can keep track of the observations
        self.browser.find_element_by_link_text('Observation log').click()

        #Here he sees a form to submit his observations
        self.browser.find_element_by_id('id_obs_date').send_keys("2017-01-01")
        self.browser.find_element_by_id('id_obs_type').send_keys('S')
        self.browser.find_element_by_id('id_telescope').send_keys("NTT")
        self.browser.find_element_by_id('id_instrument').send_keys("EFOSC2")
        self.browser.find_element_by_id('id_setup').send_keys("GR13")
        self.browser.find_element_by_id('id_notes').send_keys("Trial")
        self.browser.find_element_by_tag_name("button").click()

        #He made a mistake, and wants to edit the entry
        self.browser.find_element_by_css_selector(".fa-pencil").click()
        setup=self.browser.find_element_by_id('id_setup').get_attribute('value')
        self.assertEqual("GR13", setup)
        self.browser.find_element_by_id('id_setup').send_keys("GR13, GR16\n")

        #Now he wants to add a new entry
        self.browser.find_element_by_id('id_obs_date').send_keys("2017-01-02")
        self.browser.find_element_by_id('id_obs_type').send_keys('P')
        self.browser.find_element_by_id('id_telescope').send_keys("NTT")
        self.browser.find_element_by_id('id_instrument').send_keys("EFOSC2")
        self.browser.find_element_by_id('id_setup').send_keys("B")
        self.browser.find_element_by_id('id_notes').send_keys("Trial2")
        self.browser.find_element_by_tag_name("button").click()
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn("GR13, GR16", body)
        self.assertIn("B", body)
