from django.shortcuts import render

# Create your views here.
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib.auth import authenticate
from wechat.models import *
from WeChatDiudiu.settings import TICKET_MENU

import urllib.parse
import urllib.request
import sys
import time
import datetime

STATUS = 0
class Login(APIView):

    def get(self):
        global STATUS
        if STATUS == 0:
            raise LogicError('Not logged in!')

    def post(self):
        global STATUS
        self.check_input('username','password')
        user = authenticate(username = self.input['username'], password = self.input['password'])
        if user == None:
            raise ValidateError('Invalid admin username or password!')
        STATUS = 1

class Logout(APIView):

    def post(self):
        global STATUS
        try:
            STATUS = 0
        except:
            raise LogicError('Logout failed!')

class ActivityList(APIView):

    def get(self):
        activities = Activity.objects.all()
        list = []
        for activity in activities:
            if activity.status < 0:
                continue
            res = {
                'id': activity.id,
                'name': activity.name,
                'startTime': int(
                    time.mktime(time.strptime(str(activity.start_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                'endTime': int(time.mktime(time.strptime(str(activity.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                'bookStart': int(
                    time.mktime(time.strptime(str(activity.book_start)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                'bookEnd': int(time.mktime(time.strptime(str(activity.book_end)[0:-6], "%Y-%m-%d %H:%M:%S"))),
                'place': activity.place,
                'description': activity.description,
                'status': activity.status,
                'currentTime': int(time.mktime(time.strptime(str(datetime.datetime.now())[0:-7], "%Y-%m-%d %H:%M:%S")))
            }
            list.append(res)
        return list

class ActivityDelete(APIView):

    def post(self):
        self.check_input('id')
        Activity.delete_by_id(self.input['id'])

class ActivityCreate(APIView):

    def post(self):
        self.check_input('name','key','place','description','picUrl','startTime','endTime','bookStart','bookEnd','totalTickets','status')
        return Activity.create_(self.input)

class UploadImage(APIView):

    def post(self):
        # f = open(r'activity979.bmp','w')
        # #f.write(self.input[])
        # str = self.input[' filename']
        # print(str.split("\r\n"))
        # # f.write(str.split("\r\n")[3])
        # print(self.input)
        return 'http://y2.ifengimg.com/5ac087185c03ccf0/2014/0312/rdn_5320368a178f1.png'

class ActivityDetail(APIView):

    def get(self):
        self.check_input('id')
        activity = Activity.get_by_id(self.input['id'])
        res = {
            'key': activity.key,
            'name': activity.name,
            'startTime': int(
                time.mktime(time.strptime(str(activity.start_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'endTime': int(time.mktime(time.strptime(str(activity.end_time)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'bookStart': int(
                time.mktime(time.strptime(str(activity.book_start)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'bookEnd': int(time.mktime(time.strptime(str(activity.book_end)[0:-6], "%Y-%m-%d %H:%M:%S"))),
            'currentTime': int(time.mktime(time.strptime(str(datetime.datetime.now())[0:-7], "%Y-%m-%d %H:%M:%S"))),
            'place': activity.place,
            'description': activity.description,
            'status': activity.status,
            'totalTickets': activity.total_tickets,
            'picUrl': activity.pic_url,
            'bookedTickets': activity.total_tickets - activity.remain_tickets,
            'usedTickets': 0
        }

        return res

    def post(self):
        self.check_input('name','id','place','description','picUrl','startTime','endTime','bookStart','bookEnd','totalTickets','status')
        activity = Activity.get_by_id(self.input['id'])
        activity.name = self.input['name']
        activity.place = self.input['place']
        activity.description = self.input['description']
        activity.pic_url = self.input['picUrl']
        activity.start_time = self.input['startTime']
        activity.end_time = self.input['endTime']
        activity.book_start = self.input['bookStart']
        activity.book_end = self.input['bookEnd']
        activity.total_tickets = self.input['totalTickets']
        activity.status = self.input['status']
        activity.id = self.input['id']
        activity.save()

class ActivityMenu(APIView):

    def get(self):
        activities = Activity.objects.all()
        list = []
        for activity in activities:
            index = 0
            for i in TICKET_MENU:
                index += 1
                if i == activity.id:
                    break
            if activity.id not in TICKET_MENU:
                index = 0
            if activity.status <= 0:
                continue
            res = {
                'id': activity.id,
                'name': activity.name,
                'menuIndex': index
            }
            list.append(res)
            index += 1
        return list

    def post(self):
        try:
            TICKET_MENU.clear()
            for i in self.input:
                TICKET_MENU.append(i)
        except:
            raise LogicError('Modify menu Failed')

class ActivityCheckin(APIView):

    def post(self):
        self.check_input('id')
        ticket = Ticket.objects.get(self.input['id'])
        res = {
            'ticket': ticket.id,
            'studentId': ticket.student_id
        }
        return res