import time
from models import Model


# class Reply(Model):
#     def __init__(self, form):
#         self.id = None
#         self.content = form.get('content','')
#         self.ct = int(time.time())
#         self.topic_id = int(form.get('topic_id', -1))
#
#     def user(self):
#         from .user import User
#         u = User.find(self.user_id)
#         return u
from .mongua import Mongua
import datetime
from utils import translate_time
class Reply(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('content',str,''),
        ('topic_id',int,-1),
        ('user_id',int,-1)
    ]

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    def set_user_id(self,user_id):
        self.user_id = user_id
        self.save()

    def time_count(self):
        real_time_now = translate_time(time.time())
        real_time_old = translate_time(self.update_time)

        startTime = datetime.datetime.strptime(real_time_old, "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(real_time_now, "%Y-%m-%d %H:%M:%S")

        gap_time = (endTime - startTime).seconds/(24*3600)
        # gap_time = int(gap_time/(3600*24))
        print(type(gap_time))
        return int(gap_time)