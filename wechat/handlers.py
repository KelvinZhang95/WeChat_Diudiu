# -*- coding: utf-8 -*-
#
from WeChatDiudiu import settings
from wechat.wrapper import WeChatHandler
from wechat.models import *
import time
import datetime
from django.db.models import F
import urllib.request



class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑')

    def handle(self):
        self.user.student_id = ''
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))

class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['bind_account'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))

class CheckRankHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['check_rank'])

    def handle(self):
        return self.reply_text('您的信用等级是' + str(self.user.rank) + '级')

class CheckPublishedHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['check_published'])

    def handle(self):
        return self.reply_text(self.get_message('check_published'))

class CheckClaimedHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['check_claimed'])

    def handle(self):
        return self.reply_text(self.get_message('check_claimed'))

class LostHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['lost_IDCard']) or \
               self.is_event_click(self.view.event_keys['lost_class1']) or \
               self.is_event_click(self.view.event_keys['lost_class2']) or \
               self.is_event_click(self.view.event_keys['lost_class3']) or \
               self.is_event_click(self.view.event_keys['lost_class4'])

    def handle(self):
        if self.is_event_click(self.view.event_keys['lost_IDCard']):
            res = {
                'open_id': self.user.open_id,
                'kind': -1,
            }
            cur_state = State.get_by_openid(self.user.open_id)
            if cur_state == None:
                new_state = State.create_(res)
                return self.reply_text('请输入您丢失的ID卡的号码\n（包括学生卡、身份证、银行卡等）')
            else:
                cur_state.status = 0
                cur_state.save()
                return self.reply_text('您之前未完成的登记已被重置\n请重新输入您丢失的ID卡的号码')
        else:
            return self.reply_text(self.get_message('lost_others'))

class FoundHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['found_IDCard']) or \
               self.is_event_click(self.view.event_keys['found_class1']) or \
               self.is_event_click(self.view.event_keys['found_class2']) or \
               self.is_event_click(self.view.event_keys['found_class3']) or \
               self.is_event_click(self.view.event_keys['found_class4'])

    def handle(self):
        if self.is_event_click(self.view.event_keys['found_IDCard']):
            res = {
                'open_id': self.user.open_id,
                'kind': 1,
            }
            cur_state = State.get_by_openid(self.user.open_id)
            if cur_state == None:
                new_state = State.create_(res)
                return self.reply_text('请输入您拾到的ID卡的号码\n（包括学生卡、身份证、银行卡等）')
            else:
                cur_state.status = 0
                cur_state.kind = 1
                cur_state.save()
                return self.reply_text('您之前未完成的登记已被重置\n请重新输入您拾到的ID卡的号码')
        else:
            res = {
                'open_id': self.user.open_id,
                'kind': 1 + int(self.input['EventKey'][-1]),
            }
            cur_state = State.get_by_openid(self.user.open_id)
            if cur_state == None:
                new_state = State.create_(res)
                return self.reply_text('请上传物品图片')
            else:
                cur_state.status = 0
                cur_state.kind = res['kind']
                cur_state.save()
                return self.reply_text('您之前未完成的登记已被重置\n请重新上传物品图片')

class StateHandler(WeChatHandler):

    cur_state = None

    def check(self):
        self.cur_state = State.get_by_openid(self.user.open_id)
        return (self.is_msg_type('text') or self.is_msg_type('image')) and self.cur_state != None

    def handle(self):
        if self.cur_state.kind == -1:
            if self.is_msg_type('text'):
                cur_IDCard = IDCard.get_by_idnum(self.input['Content'])
                if cur_IDCard != None and cur_IDCard.status == 0:
                    self.cur_state.delete()
                    if cur_IDCard.kind == -1:
                        return self.reply_text('卡号错误')
                    else:
                        cur_IDCard.open_id_lost = self.user.open_id
                        cur_IDCard.status = 1
                        cur_IDCard.end_time = datetime.datetime.now()
                        cur_IDCard.save()
                        return self.reply_text('已经有人拾到您的卡了\n他的联系方式是：\n' + cur_IDCard.contact_way + '\n快去联系Ta吧！')
                else:
                    if self.cur_state.status == 0:
                        self.cur_state.status = 1
                        self.cur_state.object1 = self.input['Content']
                        self.cur_state.save()
                        return self.reply_text('请继续留下您的联系方式')
                    elif self.cur_state.status == 1:
                        self.cur_state.status = 2
                        self.cur_state.object2 = self.input['Content']
                        self.cur_state.save()
                        res = {
                            'open_id_lost': self.user.open_id,
                            'open_id_found': '',
                            'id_num': self.cur_state.object1,
                            'contact_way': self.cur_state.object2,
                            'kind': self.cur_state.kind
                        }
                        IDCard.create_(res)
                        self.cur_state.delete()
                        return self.reply_text('已经为您登记丢失信息，如果有人拾到您的卡，Ta会立即联系您。')
            else:
                return self.reply_text('错误的输入类型，请按要求继续')
        elif self.cur_state.kind == 1:
            if self.is_msg_type('text'):
                cur_IDCard = IDCard.get_by_idnum(self.input['Content'])
                if cur_IDCard != None and cur_IDCard.status == 0:
                    self.cur_state.delete()
                    if cur_IDCard.kind == 1:
                        return self.reply_text('卡号错误')
                    else:
                        cur_IDCard.open_id_found = self.user.open_id
                        cur_IDCard.status = 1
                        cur_IDCard.end_time = datetime.datetime.now()
                        cur_IDCard.save()
                        return self.reply_text('它主人正在寻找这张卡片，\nTa的联系方式是：\n' + cur_IDCard.contact_way + '\n快去联系Ta吧！')
                else:
                    if self.cur_state.status == 0:
                        self.cur_state.status = 1
                        self.cur_state.object1 = self.input['Content']
                        self.cur_state.save()
                        return self.reply_text('请继续留下您的联系方式')
                    elif self.cur_state.status == 1:
                        self.cur_state.status = 2
                        self.cur_state.object2 = self.input['Content']
                        self.cur_state.save()
                        res = {
                            'open_id_found': self.user.open_id,
                            'open_id_lost': '',
                            'id_num': self.cur_state.object1,
                            'contact_way': self.cur_state.object2,
                            'kind': self.cur_state.kind
                        }
                        IDCard.create_(res)
                        self.cur_state.delete()
                        return self.reply_text('已经为您登记该卡信息，请暂存该卡片，等待失主联系。')
            else:
                return self.reply_text('错误的输入类型，请按要求继续')
        elif self.cur_state.kind >= 2:
            if self.cur_state.status == 0:
                if self.is_msg_type('image'):
                    self.cur_state.status = 1
                    self.cur_state.object1 = self.input['PicUrl']
                    self.cur_state.save()
                    return self.reply_text('请作简要描述，如拾取地点、物品特征')
                else:
                    return self.reply_text('请点击聊天框右边按钮，上传物品图片')
            elif self.cur_state.status == 1:
                if self.is_msg_type('text'):
                    self.cur_state.status = 2
                    self.cur_state.object2 = self.input['Content']
                    self.cur_state.save()
                    return self.reply_text('请继续留下您的联系方式')
                else:
                    return self.reply_text('请以文字形式留下您的联系方式')
            elif self.cur_state.status == 2:
                if self.is_msg_type('text'):
                    self.cur_state.status = 3
                    self.cur_state.object3 = self.input['Content']
                    self.cur_state.save()
                    filename = self.user.open_id[-5:-1] + str(int(time.time()))
                    new_url = settings.get_url('image/') + filename
                    urllib.request.urlretrieve(self.cur_state.object1, 'static/image/' + filename)
                    res = {
                        'open_id_found': self.user.open_id,
                        'open_id_lost': '',
                        'pic_url': new_url,
                        'description': self.cur_state.object2,
                        'contact_way': self.cur_state.object3,
                        'kind': self.cur_state.kind
                    }
                    Others.create_(res)
                    self.cur_state.delete()
                    return self.reply_text('已经为您登记该物品信息，请暂存该物品，等待失主联系。')
                else:
                    return self.reply_text('请用文字简要描述，如拾取地点、物品特征')
