from django.test import TestCase
import unittest
from unittest.mock import Mock, patch, MagicMock
from wechat.models import *
from wechat.views import CustomWeChatView
from wechat.handlers import *
from wechat.wrapper import WeChatView, WeChatHandler, WeChatEmptyHandler
from codex.baseerror import *
# Create your tests here


class UserType:
    open_id = '1'


class GetTest(TestCase):

    def test_error_handler(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'text'}
        eh = ErrorHandler(wcw, message, 1)
        self.assertTrue(eh.check())
        self.assertNotEqual(eh.handle().find('服务器现在有点忙'), -1)

    def test_default_handler(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'text'}
        dh = DefaultHandler(wcw, message, 1)
        self.assertTrue(dh.check())
        self.assertNotEqual(dh.handle().find('没有找到您需要的信息'), -1)

    def test_bind_handler(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'event', 'Event' : 'CLICK', 'EventKey' : 'BIND_ACCOUNT'}
        h = BindAccountHandler(wcw, message, 1)
        self.assertTrue(h.check())
        #h.handle()

    def test_unbind_handler(self):
        wcw = CustomWeChatView
        message = {'Content': '解绑', 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'text'}
        h = UnbindOrUnsubscribeHandler(wcw, message, 1)
        self.assertTrue(h.check())
        #h.handle()

    def test_check_rank_handler(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'Event' : 'CLICK', 'EventKey' : 'CHECK_RANK'}
        h = DefaultHandler(wcw, message, 1)
        self.assertTrue(h.check())
        #self.assertNotEqual(h.handle().find('您的信用等级是'), -1)

    def test_check_published_handler(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'Event' : 'CLICK', 'EventKey' : 'CHECK_PUBLISHED'}
        h = DefaultHandler(wcw, message, 1)
        self.assertTrue(h.check())
        print('Check_published')
        print(h.handle())
        #self.assertNotEqual(h.handle().find(''), -1)#ÐÅÓÃ

    def test_check_claimed_handler(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'Event' : 'CLICK', 'EventKey' : 'CHECK_CLAIMED'}
        h = DefaultHandler(wcw, message, 1)
        self.assertTrue(h.check())
        print('Check_claimed')
        print(h.handle())
        #self.assertNotEqual(h.handle().find(''), -1)#ÐÅÓÃ

    def test_lost_IDCard_without_openid(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'event', 'Event' : 'CLICK', 'EventKey' : 'LOST_IDCARD'}
        usr = UserType
        h = LostHandler(wcw, message, usr)
        self.assertTrue(h.check())
        self.assertNotEqual(h.handle().find('请输入您丢失的ID卡的号码'), -1)

    def test_lost_IDCard_with_openid(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'event', 'Event' : 'CLICK', 'EventKey' : 'LOST_IDCARD'}
        usr = UserType
        h = LostHandler(wcw, message, usr)
        self.assertTrue(h.check())
        opid = '1'
        state_ = {'open_id' : opid, 'kind' : 1}
        State.create_(state_);
        a = h.handle()
        State.get_by_openid(opid).delete()
        self.assertNotEqual(a.find('请重新输入您丢失的ID卡的号码'), -1)

    def test_lost_others(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'event', 'Event': 'CLICK','EventKey': 'LOST_CLASS1'}
        usr = UserType
        self.assertTrue(LostHandler(wcw, message, usr).check())
        message['EventKey'] = 'LOST_CLASS2'
        self.assertTrue(LostHandler(wcw, message, usr).check())
        message['EventKey'] = 'LOST_CLASS3'
        self.assertTrue(LostHandler(wcw, message, usr).check())
        message['EventKey'] = 'LOST_CLASS4'
        self.assertTrue(LostHandler(wcw, message, usr).check())

    def test_found_IDCard_without_openid(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'event', 'Event' : 'CLICK', 'EventKey' : 'FOUND_IDCARD'}
        usr = UserType
        fh = FoundHandler(wcw, message, usr)
        self.assertTrue(fh.check())
        a = fh.handle()
        self.assertNotEqual(a.find('请输入您拾到的ID卡的号码'), -1)

    def test_found_IDCard_with_openid(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'event', 'Event': 'CLICK',
                   'EventKey': 'FOUND_IDCARD'}
        usr = UserType
        fh = FoundHandler(wcw, message, usr)
        self.assertTrue(fh.check())
        opid = '1'
        state_ = {'open_id' : opid, 'kind' : 1}
        State.create_(state_);
        a = fh.handle()
        State.get_by_openid(opid).delete()
        self.assertNotEqual(a.find('请重新输入您拾到的ID卡的号码'), -1)

    def test_found_Class1_without_openid(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'event', 'Event': 'CLICK',
                   'EventKey': 'FOUND_CLASS1'}
        usr = UserType
        fh = FoundHandler(wcw, message, usr)
        self.assertTrue(fh.check())
        a = fh.handle()
        #print (a)
        self.assertNotEqual(a.find('请上传物品图片'), -1)

    def test_found_Class2_with_openid(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'event', 'Event': 'CLICK',
                   'EventKey': 'FOUND_CLASS2'}
        usr = UserType
        fh = FoundHandler(wcw, message, usr)
        self.assertTrue(fh.check())
        opid = '1'
        state_ = {'open_id' : opid, 'kind' : 1}
        State.create_(state_);
        a = fh.handle()
        State.get_by_openid(opid).delete()
        self.assertNotEqual(a.find('您之前未完成的登记已被重置\n请重新上传物品图片'), -1)

    def test_found_others(self):
        wcw = CustomWeChatView
        message = {'Content': 1, 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'event', 'Event': 'CLICK',
                   'EventKey': 'FOUND_CLASS3'}
        usr = UserType
        self.assertTrue(FoundHandler(wcw, message, usr).check())
        message['EventKey'] = 'FOUND_CLASS4'
        self.assertTrue(FoundHandler(wcw, message, usr).check())

    def test_state_without_openid(self):
        wcw = CustomWeChatView
        message = {'Content': '1', 'ToUserName' : '3', 'FromUserName' : '4', 'MsgType' : 'text'}
        usr = UserType
        sh = StateHandler(wcw, message, usr)
        self.assertFalse(sh.check())

    def test_state_kind0(self):
        wcw = CustomWeChatView
        message = {'Content': 3, 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'text'}
        usr = UserType
        sh = StateHandler(wcw, message, usr)
        #1. not in database
        opid = '123'
        state_ = {'open_id': opid, 'kind': -1}
        State.create_(state_)
        sh.cur_state = State.get_by_openid(opid)
        print('kind = ' + str(sh.cur_state.kind) + ' ' + str(sh.cur_state.id))
        #status = 0
        sh.cur_state.status = 0
        self.assertNotEqual(sh.handle().find('请继续留下您的联系方式'), -1)
        #status = 1
        sh.cur_state.status = 1
        sh.cur_state.object1 = '233'
        self.assertNotEqual(sh.handle().find('已经为您登记丢失信息'), -1)
        IDCard.objects.filter(id_num='233').delete()#delete the record that was added in handle()
        #2. in database
        res = {
            'open_id_lost': 'abc',
            'open_id_found': 'cba',
            'id_num': '3',
            'contact_way': '123',
            'kind': 1
        }
        IDCard.create_(res)
        State.create_(state_)
        sh.cur_state = State.get_by_openid(opid)
        self.assertNotEqual(sh.handle().find('已经有人拾到您的卡了'), -1)
        IDCard.objects.filter(id_num='3').delete()

    def test_state_kind1(self):
        wcw = CustomWeChatView
        message = {'Content': 3, 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'text'}
        usr = UserType
        sh = StateHandler(wcw, message, usr)
        #1. not in database
        opid = '123'
        state_ = {'open_id': opid, 'kind': 1}
        State.create_(state_)
        sh.cur_state = State.get_by_openid(opid)
        #status = 0
        sh.cur_state.status = 0
        self.assertNotEqual(sh.handle().find('请继续留下您的联系方式'), -1)
        #status = 1
        sh.cur_state.status = 1
        sh.cur_state.object1 = '233'
        self.assertNotEqual(sh.handle().find('已经为您登记该卡信息，请暂存该卡片，等待失主联系'), -1)
        IDCard.objects.filter(id_num='233').delete()#delete the record that was added in handle()
        #2. in database
        res = {
            'open_id_lost': 'abc',
            'open_id_found': 'cba',
            'id_num': '3',
            'contact_way': '123',
            'kind': 2
        }
        IDCard.create_(res)
        State.create_(state_)
        sh.cur_state = State.get_by_openid(opid)
        #print(sh.handle())
        self.assertNotEqual(sh.handle().find('它主人正在寻找这张卡片'), -1)
        IDCard.objects.filter(id_num='3').delete()

    def test_state_kind2(self):
        wcw = CustomWeChatView
        message = {'Content': '2', 'ToUserName': '3', 'FromUserName': '4', 'MsgType': 'image', 'PicUrl' : 'a'}
        usr = UserType
        sh = StateHandler(wcw, message, usr)
        sh.cur_state = State()
        sh.cur_state.kind = 2
        #status = 0
        sh.cur_state.status = 0
        self.assertNotEqual(sh.handle().find('请作简要描述'), -1)
        #status = 1
        sh.cur_state.status = 1
        sh.input['MsgType'] = 'text'
        self.assertNotEqual(sh.handle().find('请继续留下您的联系方式'), -1)
        #status = 2
        sh.cur_state.status = 2
        #sh.handle()