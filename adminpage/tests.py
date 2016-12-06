from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve

import json
import adminpage.urls
import unittest
from unittest.mock import Mock, patch, MagicMock
from wechat.models import User

from codex.baseerror import *

from adminpage.views import *

# Create your tests here.

class URLTest(TestCase):
    def test_a_activity_checkin(self):
        response = self.client.get('/a/activity/checkin')
        self.assertContains(response, '检票')

    def test_a_activity_detail(self):
        response = self.client.get('/a/activity/detail')
        self.assertContains(response, '新建活动')

    def test_a_activity_list(self):
        response = self.client.get('/a/activity/list')
        self.assertContains(response, '活动列表')

    def test_a_activity_menu(self):
        response = self.client.get('/a/activity/menu')
        self.assertContains(response, '设置抢票菜单')

    def test_a_login(self):
        response = self.client.get('/a/login')
        self.assertContains(response, '登录')