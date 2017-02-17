from .base import FunctionalTest

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
        self.browser.find_element_by_id('id_notes').send_keys('ntt\n')

        #After submitting the form, the data appears in a table
        self.browser.find_element_by_tag_name("table")
