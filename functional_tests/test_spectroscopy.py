from .base import FunctionalTest

class SpectroscopyTest(FunctionalTest):

    def test_user_can_add_reduced_spectrum_at_spectra_page(self):
        #Joe goes to the SN page, adds a new SN
        self.browser.get(self.server_url)
        self.add_new_sn()

        #Redirected to the SN's page, Joe notices that here he can keep track of the reduced spectra of the SN
        self.browser.find_element_by_link_text('Spectroscopy').click()

        #It leads him to the Spectroscopy page
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn('SN 1987A - Spectroscopy', body)

        #Here he sees a form to submit a spectra as a file
        self.browser.find_element_by_id("id_file").send_keys("/home/kati/Dropbox/munka/learning/sn_app/test_tools/test_spectrum.dat")
        self.browser.find_element_by_id('id_uploadbutton').click()

        #After sending the file, the data appears in a table
        body=self.browser.find_element_by_tag_name("body").text
        self.fail()
        self.assertIn('55213.1', body)
