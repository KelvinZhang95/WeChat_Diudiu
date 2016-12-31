# coding=utf-8
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import os
from wechat.models import Others, User

class UserPageTest(StaticLiveServerTestCase):
    fixtures = ['users.json']
    browser = None

    @classmethod
    def setUpClass(cls):
        super(UserPageTest, cls).setUpClass()
        cls.browser = webdriver.PhantomJS()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(UserPageTest, cls).tearDownClass()

    def test_lost_list(self):
        server_url = 'http://59.116.160.106'
        self.browser.get('%s%s' % (server_url, '/u/lost/list?kind=2'))

    def test_lost_detail(self):
        server_url = 'http://59.116.160.106'
        self.browser.get('%s%s' % (server_url, '/u/lost/detail?id=1'))

