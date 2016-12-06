# -*- coding: utf-8 -*-
from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import *
from urllib.request import urlopen

from html.parser import HTMLParser
import urllib.parse
import urllib.request
import time
import datetime
import string
import re


class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """

        #raise NotImplementedError('You should implement UserBind.validate_user method')

        posturl = 'https://learn.tsinghua.edu.cn/MultiLanguage/lesson/teacher/loginteacher.jsp'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                   'Referer': 'http://learn.tsinghua.edu.cn/'}
        try:
            postData = {
                'userid': self.input['student_id'],
                'userpass': self.input['password'],
                'submit1': '登录'
            }
            # postData = urllib.parse.urlencode(postData)
            # postData = postData.encode('utf-8')
            # request = urllib.request.Request(posturl, postData, headers)
            response = urlopen(posturl,urllib.parse.urlencode(postData).encode('utf-8'))
            text = response.read()
            if(len(text) > 100):
                raise ValidateError('Validation failed!')
        except:
            raise ValidateError('')


    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()


class ActivityDetail(APIView):

    def get(self):
        self.check_input('id')
        activity = Activity.get_by_id(self.input['id'])
        res = {
            'id' : activity.id,
            'name' : activity.name,
            'startTime' : int(time.mktime(time.strptime(str(activity.start_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'endTime' : int(time.mktime(time.strptime(str(activity.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'bookStart': int(time.mktime(time.strptime(str(activity.book_start)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'bookEnd': int(time.mktime(time.strptime(str(activity.book_end)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'place' : activity.place,
            'description' : activity.description,
            'key' : activity.key,
            'totalTickets' : activity.total_tickets,
            'picUrl' : activity.pic_url,
            'remainTickets' : activity.remain_tickets,
            'currentTime' : int(time.mktime(time.strptime(str(datetime.datetime.now())[0:-7], "%Y-%m-%d %H:%M:%S")))
        }
        return res

class TicketDetail(APIView):

    def get(self):
        self.check_input('openid', 'ticket')
        ticket = Ticket.get_by_unique_id(self.input['ticket'])
        activity = Activity.get_by_id(ticket.activity_id)
        res = {
            'activityName': activity.name,
            'place': activity.place,
            'activityKey': activity.key,
            'uniqueId': ticket.unique_id,
            'startTime': int(time.mktime(time.strptime(str(activity.start_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'endTime': int(time.mktime(time.strptime(str(activity.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'currentTime': int(time.mktime(time.strptime(str(datetime.datetime.now())[0:-7], "%Y-%m-%d %H:%M:%S"))),
            'status': ticket.status
        }
        return res
