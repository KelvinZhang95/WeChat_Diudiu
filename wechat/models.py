from django.db import models

from codex.baseerror import LogicError
import datetime
import time

class User(models.Model):
    open_id = models.CharField(max_length=64, unique=True, db_index=True)
    student_id = models.CharField(max_length=32, db_index=True)
    rank = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    left_claim_num = models.IntegerField(default=5)
    last_claim_time = models.DateField(null=True)

    @classmethod
    def get_by_openid(cls, openid):
        try:
            return cls.objects.get(open_id=openid)
        except cls.DoesNotExist:
            raise LogicError('User not found')

    @classmethod
    def update_left_claim_num(cls, openid):
        try:
            user = cls.objects.get(open_id=openid)
            if user.last_claim_time != datetime.date.today():
                user.left_claim_num = 5 + user.rank
                user.save()
        except cls.DoesNotExist:
            raise LogicError('User not found')

    @classmethod
    def change_score(cls, openid, delta):
        try:
            user = cls.objects.get(open_id=openid)
            if user.student_id:
                if delta > 0:
                    user.score = user.score + delta * 2
                else:
                    user.score = user.score - delta / 2
            else:
                user.score = user.score + delta
            if user.score >= 100:
                user.score = 0
                user.rank = user.rank + 1
            elif user.score < 0:
                user.score = 50
                user.rank = user.rank - 1
            user.save()
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
    end_time = models.DateTimeField(null=True)

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
    open_id_found = models.CharField(max_length=64, db_index=True)
    open_id_lost = models.CharField(max_length=64, db_index=True)
    pic_url = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    contact_way = models.CharField(max_length=256)
    kind = models.IntegerField()
    status = models.IntegerField()
    create_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    @classmethod
    def create_(cls, res):
        try:
            obj = cls.objects.create(open_id_found=res['open_id_found'], open_id_lost=res['open_id_lost'], \
                                     pic_url=res['pic_url'], description=res['description'], contact_way=res['contact_way'], \
                                     kind=res['kind'], status=0, create_time=datetime.datetime.now())
            return obj.id
        except:
            raise LogicError('create state error!')

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.objects.get(id=id)
        except cls.DoesNotExist:
            # raise LogicError('state dose not exist!')
            return None

    @classmethod
    def get_by_kind(cls, kind_):
        return cls.objects.filter(kind = kind_)

    @classmethod
    def get_by_openid_found(cls, openid_found_):
        return cls.objects.filter(open_id_found=openid_found_)

    @classmethod
    def get_by_openid_lost(cls, openid_lost_):
        return cls.objects.filter(open_id_lost=openid_lost_)

