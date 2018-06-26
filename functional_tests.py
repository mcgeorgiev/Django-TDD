from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Visit To Do app home page
        self.browser.get('http://localhost:8000')

        # Notice the page title in the header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Invited to enter a to-do item straight away
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertIn(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Types "buy peacock feathers" into text box
        input_box.send_keys('Buy peacock feathers')

        # When hits enter, page updates, and lists todo
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in the table"
        )

        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
