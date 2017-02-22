from .base import FunctionalTest
import time

class PhotometryTest(FunctionalTest):

    def test_user_can_add_photometric_point_to_light_curve_log(self):
        #Joe goes to the SN page, adds a new SN
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Add a new SN').click()
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')

        #Redirected to the SN's page, Joe notices that here he can keep track of the photometry of the SN
        self.browser.find_element_by_link_text('Photometry').click()

        #He sees a form to submit Photometry
        self.browser.find_element_by_id('id_MJD').send_keys('57754.4')
        self.browser.find_element_by_id('id_Filter').send_keys('B')
        self.browser.find_element_by_id('id_magnitude').send_keys('15.5')
        self.browser.find_element_by_id('id_mag_error').send_keys('0.02')
        self.browser.find_element_by_id('id_notes').send_keys('ntt')
        self.browser.find_element_by_id('id_formsubmitbutton').click()
        #After submitting the form, the data appears in a table
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn('ntt', body)

    def test_user_can_upload_a_photometry_file(self):
        #Joe goes to the SN page, adds a new SN
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Add a new SN').click()
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')

        #Redirected to the SN's page, Joe notices that here he can keep track of the photometry of the SN
        self.browser.find_element_by_link_text('Photometry').click()

        #He sees that he can add photometry by uploading a file
        self.browser.find_element_by_id("id_file").send_keys("/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry.txt")
        time.sleep(5)
        self.browser.find_element_by_id('id_uploadbutton').click()

        #After sending the file, the data appears in a table
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn('55213.1', body)

        #He uploads another file, however the format of this is incorrect, so he gets an error
        self.browser.find_element_by_id("id_file").send_keys("/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry_incorrect.txt")
        self.browser.find_element_by_id('id_uploadbutton').click()
        body=self.browser.find_element_by_tag_name("body").text
        time.sleep(5)
        self.assertIn("The file format is incorrect. Please check the requirements", body)

    def test_user_can_edit_and_delete_photometric_poin(self):
        #Joe goes to the SN page, adds a new SN
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Add a new SN').click()
        self.browser.find_element_by_id("id_sn_name").send_keys('SN 1987A')
        self.browser.find_element_by_id("id_ra").send_keys('05:35:27.99')
        self.browser.find_element_by_id("id_dec").send_keys('-69:16:11.50\n')

        #Redirected to the SN's page, Joe notices that here he can keep track of the photometry of the SN
        self.browser.find_element_by_link_text('Photometry').click()

        #He sees a form to submit Photometry
        self.browser.find_element_by_id('id_MJD').send_keys('57754.4')
        self.browser.find_element_by_id('id_Filter').send_keys('B')
        self.browser.find_element_by_id('id_magnitude').send_keys('15.5')
        self.browser.find_element_by_id('id_mag_error').send_keys('0.02')
        self.browser.find_element_by_id('id_notes').send_keys('ntt')
        self.browser.find_element_by_id('id_formsubmitbutton').click()
        #After submitting the form, the data appears in a table
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn('ntt', body)
        #He also notices that one of the observations have an error, and that he can edit and correct it.
        self.browser.find_element_by_css_selector(".fa-pencil").click()
        setup=self.browser.find_element_by_id('id_magnitude').get_attribute('value')
        time.sleep(5)
        self.assertEqual("15.5", setup)
        self.browser.find_element_by_id('id_magnitude').clear()
        self.browser.find_element_by_id('id_magnitude').send_keys("15.4")
        self.browser.find_element_by_id("id_formsubmitbutton").click()
        time.sleep(5)
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("15.4", body)
        self.assertNotIn("15.5", body)

        #He also realizes that he can simply delete this entry
        self.browser.find_element_by_css_selector(".fa-trash-o").click()
        self.browser.find_element_by_link_text("OK").click()
        body=self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("15.4", body)
