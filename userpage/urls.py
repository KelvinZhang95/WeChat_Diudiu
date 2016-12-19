# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/bind/?$', UserBind.as_view()),
    url(r'^lost/list/?$', LostList.as_view()),
    url(r'^lost/detail/?$', LostDetail.as_view()),
]
