# coding=utf-8
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import os


class UserPageTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    browser = None

    @classmethod
    def setUpClass(cls):
        super(UserPageTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()
        cls.username = os.environ.get('username', '')
        cls.password = os.environ.get('password', '')

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UserPageTest, cls).tearDownClass()

    def test_bind_user(self):
        self.browser.get('%s%s' % (self.live_server_url, '/u/bind?openid=1'))

        name_box = WebDriverWait(self.browser, 10).until(expected_conditions.presence_of_element_located((By.ID, 'inputUsername')))
        name_box.send_keys(self.username)

        namebox = self.browser.find_element_by_id('inputUsername')
        namebox.send_keys(self.username)

        passwordbox = self.browser.find_element_by_id('inputPassword')
        passwordbox.send_keys(self.password)

        submit_button = self.browser.find_element_by_css_selector('#validationHolder button')
        submit_button.click()

        self.assertIn('认证', self.browser.find_element_by_id('mainbody').text)

    # def test_showticket_user(self):
    #     self.browser.get('%s%s' % (self.live_server_url, '/u/ticket?ticket=1'))
    #
    #     #submit_id = self.browser.find_element_by_css_selector('#wrap id')
    #
    #     body = self.browser.find_element_by_id('mainbody')
    #
    #     self.assertIn('111', body.get_attribute('textContent'))
    #
    # def test_checkactivity(self):
    #     self.browser.get('%s%s' % (self.live_server_url, '/u/ticket?ticket=1'))
    #
    #     self.assertIn('活', )