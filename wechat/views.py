from django.utils import timezone

from wechat.wrapper import WeChatView, WeChatLib
from wechat.handlers import *
#from wechat.models import Activity
from WeChatDiudiu.settings import WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET


class CustomWeChatView(WeChatView):

    lib = WeChatLib(WECHAT_TOKEN, WECHAT_APPID, WECHAT_SECRET)

    handlers = [
        LostHandler, FoundHandler, StateHandler, CalculateHandler,
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
            }
        ]
    }

    # @classmethod
    # def get_book_btn(cls):
    #     return cls.menu['button'][-1]
    #
    # @classmethod
    # def update_book_button(cls, activities):
    #     book_btn = cls.get_book_btn()
    #     if len(activities) == 0:
    #         book_btn['type'] = 'click'
    #         book_btn['key'] = cls.event_keys['book_empty']
    #     else:
    #         book_btn.pop('type', None)
    #         book_btn.pop('key', None)
    #     book_btn['sub_button'] = list()
    #     for act in activities:
    #         book_btn['sub_button'].append({
    #             'type': 'click',
    #             'name': act['name'],
    #             'key': cls.event_keys['book_header'] + str(act['id']),
    #         })
    #
    @classmethod
    def update_menu(cls):
        """
        :param activities: list of Activity
        :return: None
        """
        cls.lib.set_wechat_menu(cls.menu)
