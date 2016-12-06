from django.db import models

from codex.baseerror import LogicError
import datetime
import time

class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    student_id = models.CharField(max_length=32, db_index=True)

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')

class State(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    kind = models.IntegerField()
    status = models.IntegerField()
    object1 = models.CharField(max_length=256)
    object2 = models.CharField(max_length=256)
    object3 = models.CharField(max_length=256)

    @classmethod
    def create_(cls, res):
        try:
            obj = cls.objects.create(open_id=res['open_id'],kind=res['kind'],status=0)
            return obj.id
        except:
            raise LogicError('create state error!')

    @classmethod
    def get_by_openid(cls, open_id_):
        try:
            return cls.objects.get(open_id=open_id_)
        except cls.DoesNotExist:
            return None
#           raise LogicError('state dose not exist!')


class IDCard(models.Model):
    open_id_found = models.CharField(max_length=64, db_index=True)
    open_id_lost = models.CharField(max_length=64, db_index=True)
    id_num = models.CharField(max_length=64, db_index=True)
    contact_way = models.CharField(max_length=256)
    kind = models.IntegerField()
    status = models.IntegerField()
    create_time = models.DateTimeField()
    end_time = models.DateField(null=True)

    @classmethod
    def create_(cls, res):
        try:
            obj = cls.objects.create(open_id_found=res['open_id_found'], open_id_lost=res['open_id_lost'], \
                                     id_num=res['id_num'], contact_way=res['contact_way'], kind=res['kind'], \
                                     status=0, create_time=datetime.datetime.now())
            return obj.id
        except:
            raise LogicError('create state error!')

    @classmethod
    def get_by_idnum(cls, id_num_):
        try:
            return cls.objects.get(id_num = id_num_)
        except cls.DoesNotExist:
            #raise LogicError('state dose not exist!')
            return None


class Others(models.Model):
    open_id = models.CharField(max_length=64, db_index=True)
    pic_url = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    contact_way = models.CharField(max_length=256)
    kind = models.IntegerField()
    create_time = models.DateTimeField()

# class Activity(models.Model):
#     name = models.CharField(max_length=128)
#     key = models.CharField(max_length=64, db_index=True)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     place = models.CharField(max_length=256)
#     book_start = models.DateTimeField(db_index=True)
#     book_end = models.DateTimeField(db_index=True)
#     total_tickets = models.IntegerField()
#     status = models.IntegerField()
#     pic_url = models.CharField(max_length=256)
#     remain_tickets = models.IntegerField()
#
#     STATUS_DELETED = -1
#     STATUS_SAVED = 0
#     STATUS_PUBLISHED = 1
#
#     @classmethod
#     def get_by_id(cls, id_):
#         try:
#             return cls.objects.get(id=id_)
#         except cls.DoesNotExist:
#             raise LogicError('Activity not found')
#
#     @classmethod
#     def delete_by_id(cls, id_):
#         try:
#             obj = cls.objects.get(id=id_)
#             obj.status = -1
#             obj.save()
#         except:
#             raise LogicError('Delete failed')
#
#     @classmethod
#     def create_(cls, res):
#         try:
#             obj = cls.objects.create(name=res['name'],key=res['key'],place=res['place'],description=res['description'],pic_url=res['picUrl'],start_time=res['startTime'],end_time=res['endTime'],book_start=res['bookStart'],book_end=res['bookEnd'],total_tickets=res['totalTickets'],status=res['status'],remain_tickets=res['totalTickets'])
#             return obj.id
#         except:
#             raise LogicError('create activity error!')
#
#
# class Ticket(models.Model):
#     student_id = models.CharField(max_length=32, db_index=True)
#     unique_id = models.CharField(max_length=64, db_index=True, unique=True)
#     activity = models.ForeignKey(Activity)
#     status = models.IntegerField()
#
#     STATUS_CANCELLED = 0
#     STATUS_VALID = 1
#     STATUS_USED = 2
#
#     @classmethod
#     def get_by_unique_id(cls, id_):
#         try:
#             return cls.objects.get(unique_id=id_)
#         except cls.DoesNotExist:
#             raise LogicError('Ticket not found')
#
#     @classmethod
#     def create_(cls, res):
#         try:
#             obj = cls.objects.create(student_id=res['student_id'], unique_id=str(datetime.datetime.now())+str(cls.objects.count()), activity=res['activity'], status=1)
#             obj.unique_id = obj.id
#             obj.save()
#             return obj.id
#         except:
#             raise LogicError('create ticket error!')