from .base import FunctionalTest
import time
from decouple import config

TEST_TOOLS_PATH=config('TEST_TOOLS')

class SpectroscopyTest(FunctionalTest):
    def test_user_can_add_and_remove_reduced_spectrum_at_spectra_page(self):
        # Joe goes to the SN page, adds a new SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        # Redirected to the SN's page, Joe notices that here he can keep track of the reduced spectra of the SN
        self.browser.find_element_by_link_text('Spectroscopy').click()

        # It leads him to the Spectroscopy page
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn('SN 1987A', body)

        # Here he sees a form to submit a spectra as a file
        self.browser.find_element_by_id("id_MJD").send_keys("55043.2")
        self.browser.find_element_by_id("id_file").send_keys(
            TEST_TOOLS_PATH + "test_spectrum.txt")
        self.browser.find_element_by_id("id_notes").send_keys("test spectrum")
        self.browser.find_element_by_id('id_uploadbutton').click()

        # After sending the file, the data appears in a table
        body = self.browser.find_element_by_tag_name("body").text
        time.sleep(5)
        self.assertIn('55043.2', body)
        self.assertIn('test spectrum', body)

        # He uploads another spectrum
        self.browser.find_element_by_id("id_MJD").send_keys("55053.3")
        self.browser.find_element_by_id("id_file").send_keys(
            TEST_TOOLS_PATH + "test_spectrum2.txt")
        self.browser.find_element_by_id("id_notes").send_keys("Second test spectrum")
        self.browser.find_element_by_id('id_uploadbutton').click()

        # He tries to upload a pdf
        self.browser.find_element_by_id("id_MJD").send_keys("55053.3")
        self.browser.find_element_by_id("id_file").send_keys(
            TEST_TOOLS_PATH + "test.pdf")
        self.browser.find_element_by_id("id_notes").send_keys("Thirs test spectrum")
        self.browser.find_element_by_id('id_uploadbutton').click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("Incorrect file type", body)

        # Now both spectra are in the table
        body = self.browser.find_element_by_tag_name("body").text
        time.sleep(5)
        self.assertIn('55043.2', body)
        self.assertIn('55053.3', body)

        # There's also a button in the table to delete the spectrum if necessary

        self.browser.find_element_by_css_selector(".fa-trash-o").click()
        time.sleep(2)
        self.browser.find_element_by_id("id_deletebutton").click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn('55053.3', body)
        self.assertNotIn('55043.2', body)

    def test_user_can_delete_multiple_spectra(self):
        # Joe goes to the SN page, adds a new SN
        self.go_to_page_and_log_in()
        self.add_new_sn()

        # Redirected to the SN's page, Joe notices that here he can keep track of the reduced spectra of the SN
        self.browser.find_element_by_link_text('Spectroscopy').click()

        # It leads him to the Spectroscopy page
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn('SN 1987A', body)

        # Here he sees a form to submit a spectra as a file
        self.browser.find_element_by_id("id_MJD").send_keys("55043.2")
        self.browser.find_element_by_id("id_file").send_keys(
            TEST_TOOLS_PATH + "test_spectrum.txt")
        self.browser.find_element_by_id("id_notes").send_keys("test spectrum")
        self.browser.find_element_by_id('id_uploadbutton').click()

        # He uploads another spectrum
        self.browser.find_element_by_id("id_MJD").send_keys("55053.3")
        self.browser.find_element_by_id("id_file").send_keys(
            TEST_TOOLS_PATH + "test_spectrum2.txt")
        self.browser.find_element_by_id("id_notes").send_keys("Second test spectrum")
        self.browser.find_element_by_id('id_uploadbutton').click()

        # He decides to delete both spectra at once
        self.browser.find_element_by_css_selector(".selection").click()
        self.browser.find_element_by_id("id_deleteselection").click()
        time.sleep(2)
        self.browser.find_element_by_id("id_deletebutton").click()
        body = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn('55053.3', body)
        self.assertNotIn('55043.3', body)
