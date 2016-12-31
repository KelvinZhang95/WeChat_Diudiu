from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
#from wechat.models import Activity
from WeChatDiudiu.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        LostHandler, FoundHandler, StateHandler, UnbindOrUnsubscribeHandler, BindAccountHandler, CheckRankHandler, \
        CheckPublishedHandler, CheckClaimedHandler
    ]
    error_message_handler = ErrorHandler
    default_handler = DefaultHandler

    event_keys = {
        'found_IDCard': 'FOUND_IDCARD',
        'found_class1': 'FOUND_CLASS1',
        'found_class2': 'FOUND_CLASS2',
        'found_class3': 'FOUND_CLASS3',
        'found_class4': 'FOUND_CLASS4',
        'lost_IDCard': 'LOST_IDCARD',
        'lost_class1': 'LOST_CLASS1',
        'lost_class2': 'LOST_CLASS2',
        'lost_class3': 'LOST_CLASS3',
        'lost_class4': 'LOST_CLASS4',
        'bind_account': 'BIND_ACCOUNT',
        'check_rank': 'CHECK_RANK',
        'check_published': 'CHECK_PUBLISHED',
        'check_claimed': 'CHECK_CLAIMED',
    }

    menu = {
        'button': [
            {
                "name": "我是拾主",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "ID卡类",
                        "key": event_keys['found_IDCard'],
                    },
                    {
                        "type": "click",
                        "name": "钱包 钥匙",
                        "key": event_keys['found_class1'],
                    },
                    {
                        "type": "click",
                        "name": "水杯 雨伞",
                        "key": event_keys['found_class2'],
                    },
                    {
                        "type": "click",
                        "name": "电子产品",
                        "key": event_keys['found_class3'],
                    },
                    {
                        "type": "click",
                        "name": "其他物品",
                        "key": event_keys['found_class4'],
                    }
                ]
            },
            {
                "name": "我是失主",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "ID卡类",
                        "key": event_keys['lost_IDCard'],
                    },
                    {
                        "type": "click",
                        "name": "钱包 钥匙",
                        "key": event_keys['lost_class1'],
                    },
                    {
                        "type": "click",
                        "name": "水杯 雨伞",
                        "key": event_keys['lost_class2'],
                    },
                    {
                        "type": "click",
                        "name": "电子产品",
                        "key": event_keys['lost_class3'],
                    },
                    {
                        "type": "click",
                        "name": "其他物品",
                        "key": event_keys['lost_class4'],
                    }
                ]
            },
            {
                "name": "其它功能",
                "sub_button": [
                    {
                        "type": "click",
                        "name": "绑定学号",
                        "key": event_keys['bind_account'],
                    },
                    {
                        "type": "click",
                        "name": "查看积分",
                        "key": event_keys['check_rank'],
                    },
                    {
                        "type": "click",
                        "name": "已发布物品",
                        "key": event_keys['check_published'],
                    },
                    {
                        "type": "click",
                        "name": "已认领物品",
                        "key": event_keys['check_claimed'],
                    }
                ]
            }
        ]
    }

    @classmethod
    def update_menu(cls):
        cls.lib.set_wechat_menu(cls.menu)
