from selenium import webdriver
import unittest

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
        self.fail('Finish the test!')

        # Invited to enter a to-do item straight away

        # ...

if __name__ == '__main__':
    unittest.main(warnings='ignore')
