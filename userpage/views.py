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

class LostList(APIView):

    def get(self):
        self.check_input('kind')
        items = Others.get_by_kind(self.input['kind'])
        res = []
        for item in items:
            if item.status == 0:
                founder = User.get_by_openid(item.open_id_found)
                res.append(
                    {
                        'id': item.id,
                        'createTime': int(time.mktime(time.strptime(str(item.create_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                        'picUrl': item.pic_url,
                        'founderRank': founder.rank,
                    }
                )
        res = sorted(res, key=lambda x: x['createTime'], reverse=True)
        return res

class LostDetail(APIView):

    def get(self):
        self.check_input('id')
        item = Others.get_by_id(self.input['id'])
        founder = User.get_by_openid(item.open_id_found)
        res = {
            'id': item.id,
            'createTime': int(time.mktime(time.strptime(str(item.create_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'picUrl': item.pic_url,
            'description': item.description,
            'contactWay': item.contact_way,
            'founderRank': founder.rank,
        }
        return res

    def post(self):
        self.check_input('openid_lost', 'id')
        item = Others.get_by_id(self.input['id'])
        #if item.status == 1:
        #   raise ValidateError('item status error')
        User.update_left_claim_num(self.input['openid_lost'])
        user = User.get_by_openid(self.input['openid_lost'])
        if(user.left_claim_num > 0):
            user.left_claim_num = user.left_claim_num - 1
            user.last_claim_time = datetime.date.today()
            item.open_id_lost = self.input['openid_lost']
            item.end_time = datetime.datetime.now()
            item.status = 1
            item.save()
            user.save()
        else:
            raise ValidateError('no more left claim num')

class CheckPublishedList(APIView):

    def get(self):
        self.check_input('openid_found')
        items = Others.get_by_openid_found(self.input['openid_found'])
        res = []
        for item in items:
            res.append(
                {
                    'id': item.id,
                    'createTime': int(time.mktime(time.strptime(str(item.create_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                    'picUrl': item.pic_url,
                    'status': item.status,
                }
            )
        res = sorted(res, key=lambda x: x['createTime'], reverse=True)
        return res

class CheckPublishedDetail(APIView):

    def get(self):
        self.check_input('id')
        item = Others.get_by_id(self.input['id'])
        if(item.status > 0):
            res = {
                'id': item.id,
                'createTime': int(time.mktime(time.strptime(str(item.create_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                'picUrl': item.pic_url,
                'description': item.description,
                'contactWay': item.contact_way,
                'status': item.status,
                'endTime': int(time.mktime(time.strptime(str(item.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            }
        else:
            res = {
                'id': item.id,
                'createTime': int(time.mktime(time.strptime(str(item.create_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                'picUrl': item.pic_url,
                'description': item.description,
                'contactWay': item.contact_way,
                'status': item.status,
            }
        return res

    def post(self):
        self.check_input('flag', 'id')
        item = Others.get_by_id(self.input['id'])
        if self.input['flag'] == 1:
            User.change_score(item.open_id_lost, -5)
            item.status = 0
            item.save()
        elif self.input['flag'] == 0:
            item.delete()

class CheckClaimedList(APIView):

    def get(self):
        self.check_input('openid_lost')
        items = Others.get_by_openid_lost(self.input['openid_lost'])
        res = []
        for item in items:
            if item.status > 0:
                res.append(
                    {
                        'id': item.id,
                        'endTime': int(time.mktime(time.strptime(str(item.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                        'picUrl': item.pic_url,
                        'status': item.status,
                    }
                )
        res = sorted(res, key=lambda x: x['endTime'], reverse=True)
        return res

class CheckClaimedDetail(APIView):

    def get(self):
        self.check_input('id')
        item = Others.get_by_id(self.input['id'])
        founder = User.get_by_openid(item.open_id_found)
        res = {
            'id': item.id,
            'createTime': int(time.mktime(time.strptime(str(item.create_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'picUrl': item.pic_url,
            'description': item.description,
            'contactWay': item.contact_way,
            'status': item.status,
            'endTime': int(time.mktime(time.strptime(str(item.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'founderRank': founder.rank,
        }
        return res

    def post(self):
        self.check_input('flag', 'id')
        item = Others.get_by_id(self.input['id'])
        if self.input['flag'] == 0:
            User.change_score(item.open_id_found, 20)
            item.status = 2
            item.save()
        elif self.input['flag'] == 1:
            item.status = 0
            item.save()
        elif self.input['flag'] == 2:
            User.change_score(item.open_id_found, -5)
            item.status = 0
            item.save()

#
# class ActivityDetail(APIView):
#
#     def get(self):
#         self.check_input('id')
#         activity = Activity.get_by_id(self.input['id'])
#         res = {
#             'id' : activity.id,
#             'name' : activity.name,
#             'startTime' : int(time.mktime(time.strptime(str(activity.start_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
#             'endTime' : int(time.mktime(time.strptime(str(activity.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
#             'bookStart': int(time.mktime(time.strptime(str(activity.book_start)[0:-6], "%Y-%m-%d %H:%M:%S"))),
#             'bookEnd': int(time.mktime(time.strptime(str(activity.book_end)[0:-6], "%Y-%m-%d %H:%M:%S"))),
#             'place' : activity.place,
#             'description' : activity.description,
#             'key' : activity.key,
#             'totalTickets' : activity.total_tickets,
#             'picUrl' : activity.pic_url,
#             'remainTickets' : activity.remain_tickets,
#             'currentTime' : int(time.mktime(time.strptime(str(datetime.datetime.now())[0:-7], "%Y-%m-%d %H:%M:%S")))
#         }
#         return res
#
# class TicketDetail(APIView):
#
#     def get(self):
#         self.check_input('openid', 'ticket')
#         ticket = Ticket.get_by_unique_id(self.input['ticket'])
#         activity = Activity.get_by_id(ticket.activity_id)
#         res = {
#             'activityName': activity.name,
#             'place': activity.place,
#             'activityKey': activity.key,
#             'uniqueId': ticket.unique_id,
#             'startTime': int(time.mktime(time.strptime(str(activity.start_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
#             'endTime': int(time.mktime(time.strptime(str(activity.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
#             'currentTime': int(time.mktime(time.strptime(str(datetime.datetime.now())[0:-7], "%Y-%m-%d %H:%M:%S"))),
#             'status': ticket.status
#         }
#         return res
