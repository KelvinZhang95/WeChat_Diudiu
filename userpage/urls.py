# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *



urlpatterns = [
    url(r'^user/bind/?$', UserBind.as_view()),
    url(r'^lost/list/?$', LostList.as_view()),
    url(r'^lost/detail/?$', LostDetail.as_view()),
    url(r'^check/published/list?$', CheckPublishedList.as_view()),
    url(r'^check/published/detail?$', CheckPublishedDetail.as_view()),
    url(r'^check/claimed/list?$', CheckClaimedList.as_view()),
    url(r'^check/claimed/detail?$', CheckClaimedDetail.as_view()),
]
