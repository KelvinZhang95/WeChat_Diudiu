# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import *
import time
import datetime
from django.db.models import F


__author__ = "Epsirom"


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

class CalculateHandler(WeChatHandler):

     def check(self):
         try:
             eval(self.input['Content'])
         except:
             return False
         else:
             return True

     def handle(self):
         return self.reply_text(eval(self.input['Content']))


# class HelpOrSubscribeHandler(WeChatHandler):
#
#     def check(self):
#         return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe') or \
#                self.is_event_click(self.view.event_keys['help'])
#
#     def handle(self):
#         return self.reply_single_news({
#             'Title': self.get_message('help_title'),
#             'Description': self.get_message('help_description'),
#             'Url': self.url_help()
#         })
#
#
# class UnbindOrUnsubscribeHandler(WeChatHandler):
#
#     def check(self):
#         return self.is_text('解绑') or self.is_event('unsubscribe')
#
#     def handle(self):
#         self.user.student_id = ''
#         self.user.save()
#         return self.reply_text(self.get_message('unbind_account'))
#
#
# class BindAccountHandler(WeChatHandler):
#
#     def check(self):
#         return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])
#
#     def handle(self):
#         return self.reply_text(self.get_message('bind_account'))

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
            return self.reply_text('功能暂未开放，请期待')

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
                cur_state.save()
                return self.reply_text('您之前未完成的登记已被重置\n请重新输入您拾到的ID卡的号码')
        else:
            return self.reply_text('功能暂未开放，请期待')

class StateHandler(WeChatHandler):

    cur_state = None

    def check(self):
        self.cur_state = State.get_by_openid(self.user.open_id)
        return self.is_msg_type('text') and self.cur_state != None

    def handle(self):
        if self.cur_state.kind == -1:
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
                        'kind': -1
                    }
                    IDCard.create_(res)
                    self.cur_state.delete()
                    return self.reply_text('已经为您登记丢失信息，如果有人拾到您的卡，Ta会立即联系您。')
        elif self.cur_state.kind == 1:
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
                        'kind': 1
                    }
                    IDCard.create_(res)
                    self.cur_state.delete()
                    return self.reply_text('已经为您登记该卡信息，请暂存该卡片，等待失主联系。')





#
# class PreviewActivityHandler(WeChatHandler):
#
#     def check(self):
#         return self.is_text('活动列表') or self.is_event_click(self.view.event_keys['book_what'])
#
#     def handle(self):
#         return self.reply_text(self.get_message0('preview_activity'))
#         # activities = Activity.objects.all()
#         # sz = ''
#         # for i in activities:
#         #     sz += str(i.id) + " " + i.name + "\n"
#         # sz += "（回复活动+编号查看详情，例如:活动1）"
#         # return self.reply_text(sz)
#
# # class ActivityDetailHandler(WeChatHandler):
# #
# #     aid = 0
# #     def check(self):
# #         a = self.input['Content']
# #         c = Activity.objects.count()
# #         for i in range(1, c + 1):
# #             if a == '活动' + str(i):
# #                 self.aid = i
# #                 return True
# #         return False
# #
# #     def handle(self):
# #         if Activity.get_by_id(self.aid).status != 1:
# #             return self.reply_text("该活动暂未开放")
# #         return self.reply_text(self.get_message0('preview_activity', str(self.aid)))
#
# class PreviewTicketHandler(WeChatHandler):
#
#     def check(self):
#         return self.is_text('查票') or self.is_event_click(self.view.event_keys['get_ticket'])
#
#     def handle(self):
#         return self.reply_text(self.get_message1('preview_ticket'))
#
#
# class BookEmptyHandler(WeChatHandler):
#
#     def check(self):
#         return self.is_event_click(self.view.event_keys['book_empty'])
#
#     def handle(self):
#         return self.reply_text(self.get_message('book_empty'))
#
# class BookTicketHandler(WeChatHandler):
#
#     def check(self):
#         return self.is_event_click(self.view.event_keys['book_header'])
#
#     def handle(self):
#         act_id = int(self.input['EventKey'][17:])
#         act = Activity.get_by_id(act_id)
#         currentTime = int(time.mktime(time.strptime(str(datetime.datetime.now())[0:-7], "%Y-%m-%d %H:%M:%S")))
#         if currentTime < int(time.mktime(time.strptime(str(act.book_start)[0:-6], "%Y-%m-%d %H:%M:%S"))):
#             return self.reply_text('还没开始抢票哦')
#         elif currentTime > int(time.mktime(time.strptime(str(act.book_end)[0:-6], "%Y-%m-%d %H:%M:%S"))):
#             return self.reply_text('抢票已经结束了')
#         else:
#             if act.remain_tickets <= 0:
#                 return self.reply_text('票已经抢完了')
#             else:
#                 studentId = self.user.student_id
#                 res = {
#                     'student_id': studentId,
#                     'activity': act
#                 }
#                 Ticket.create_(res)
#                 act.remain_tickets = F('remain_tickets') - 1
#                 act.save()
#                 return self.reply_text('恭喜你抢到一张票')
