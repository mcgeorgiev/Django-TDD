from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import unittest
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retrieve_it_later_for_one_user(self):
        # Visit To Do app home page
        self.browser.get(self.live_server_url)

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
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # Add another to the to do list
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers')
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Starts a new todo list
        self.browser.get(self.live_server_url)

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        list_url = self.browser.current_url
        self.assertRegex(list_url, '/lists/.+')

        # a new user comes along
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #New user visits home home_page
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers', page_text)

        # start a new list
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')

        # enters own url
        new_list_url = self.browser.current_url
        self.assertRegex(new_list_url, '/lists/.+')
        self.assertNotEqual(new_list_url, list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
