from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve

import json
import userpage.urls
import unittest
from unittest.mock import Mock, patch, MagicMock
from wechat.models import User

from codex.baseerror import *

from userpage.views import *

# Create your tests here.
class GetTest(TestCase):
    def test_get_with_openid(self):
        found = resolve('/user/bind/', urlconf = userpage.urls)
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"openid": "1"}')
        with patch.object(User, 'get_by_openid', return_value=Mock(student_id=1)) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['code'], 0)

    def test_get_without_openid(self):
        found = resolve('/user/bind/', urlconf = userpage.urls)
        #with self.assertRaisesMessage(InputError, 'Field "openid" required'):
        request = Mock(wraps=HttpRequest(), method='GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{}')
        response = json.loads(found.func(request).content.decode())
        self.assertEqual(response['code'], 1)

    def test_validate_user_raise_error_without_input(self):
        user_bind_view = UserBind()
        with self.assertRaises(ValidateError):
            user_bind_view.validate_user()


class URLTest(TestCase):
    def test_u_bind(self):
        response = self.client.get('/u/bind')
        self.assertContains(response, '绑定学号')
