from .base import FunctionalTest
import time


class PhotometryTest(FunctionalTest):
    def test_user_can_add_photometric_point_to_light_curve_log(self):
        # Joe goes to the SN page, adds a new SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        # Redirected to the SN's page, Joe notices that here he can keep track of the photometry of the SN
        self.browser.find_element_by_link_text('Photometry').click()

        # He sees a form to submit Photometry
        self.browser.find_element_by_id('id_MJD').send_keys('57754.4')
        self.browser.find_element_by_id('id_Filter').send_keys('B')
        self.browser.find_element_by_id('id_magnitude').send_keys('15.5')
        self.browser.find_element_by_id('id_mag_error').send_keys('0.02')
        self.browser.find_element_by_id('id_notes').send_keys('ntt')
        self.browser.find_element_by_id('id_formsubmitbutton').click()
        # After submitting the form, the data appears in a table
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn('ntt', body)

    def test_user_can_upload_a_photometry_file(self):
        # Joe goes to the SN page, adds a new SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        # Redirected to the SN's page, Joe notices that here he can keep track of the photometry of the SN
        self.browser.find_element_by_link_text('Photometry').click()

        # He sees that he can add photometry by uploading a file
        self.browser.find_element_by_id("id_file").send_keys(
            "/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry.txt")
        self.browser.find_element_by_id('id_uploadbutton').click()

        # After sending the file, the data appears in a table
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn('55064.4', body)

        # He uploads another file, however the format of this is incorrect, so he gets an error
        self.browser.find_element_by_id("id_file").send_keys(
            "/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry_incorrect.txt")
        self.browser.find_element_by_id('id_uploadbutton').click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("The file format is incorrect. Please check the requirements", body)

        # He tries to upload a wrong file type
        self.browser.find_element_by_id("id_file").send_keys(
            "/home/kati/Dropbox/munka/learning/sn_app/test_tools/test.pdf")
        self.browser.find_element_by_id('id_uploadbutton').click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("Incorrect file type", body)

    def test_user_can_edit_and_delete_photometric_point(self):
        # Joe goes to the SN page, adds a new SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        # Redirected to the SN's page, Joe notices that here he can keep track of the photometry of the SN
        self.browser.find_element_by_link_text('Photometry').click()

        # He sees a form to submit Photometry
        self.browser.find_element_by_id('id_MJD').send_keys('57754.4')
        self.browser.find_element_by_id('id_Filter').send_keys('B')
        self.browser.find_element_by_id('id_magnitude').send_keys('15.5')
        self.browser.find_element_by_id('id_mag_error').send_keys('0.02')
        self.browser.find_element_by_id('id_notes').send_keys('ntt')
        self.browser.find_element_by_id('id_formsubmitbutton').click()
        # After submitting the form, the data appears in a table
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn('ntt', body)
        # He also notices that one of the observations have an error, and that he can edit and correct it.
        self.browser.find_element_by_css_selector(".fa-pencil").click()
        setup = self.browser.find_element_by_id('id_magnitude').get_attribute('value')
        self.assertEqual("15.5", setup)
        self.browser.find_element_by_id('id_magnitude').clear()
        self.browser.find_element_by_id('id_magnitude').send_keys("15.4")
        self.browser.find_element_by_id("id_formsubmitbutton").click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("15.4", body)
        self.assertNotIn("15.5", body)

        # He also realizes that he can simply delete this entry
        self.browser.find_element_by_css_selector(".fa-trash-o").click()
        time.sleep(2)
        self.browser.find_element_by_id("id_deletebutton").click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("15.4", body)

    def test_user_can_delete_multiple_or_all_photometry_points(self):
        # Joe goes to the SN page, adds a new SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        # Redirected to the SN's page, Joe notices that here he can keep track of the photometry of the SN
        self.browser.find_element_by_link_text('Photometry').click()

        # He sees that he can add photometry by uploading a file
        self.browser.find_element_by_id("id_file").send_keys(
            "/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry.txt")
        self.browser.find_element_by_id('id_uploadbutton').click()
        time.sleep(10)

        # He decides to delete some of it
        self.browser.find_element_by_css_selector(".selection").click()
        self.browser.find_element_by_id("id_deleteselection").click()
        time.sleep(2)
        self.browser.find_element_by_id("id_deletebutton").click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("212", body)

    def test_user_can_plot_light_curve(self):
        # Joe goes to the SN page, adds a new SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        # He uploads his photometry file
        self.browser.find_element_by_link_text('Photometry').click()
        self.browser.find_element_by_id("id_file").send_keys(
            "/home/kati/Dropbox/munka/learning/sn_app/test_tools/photometry_incorrect.txt")
        self.browser.find_element_by_id('id_uploadbutton').click()
        time.sleep(10)

        # He sees a button promising to plot the light curve
        self.browser.find_element_by_id("id_plotbutton").click()
        buttontext = self.browser.find_element_by_id("id_plotbutton").text
        self.assertEqual(buttontext, "Hide light curve")
