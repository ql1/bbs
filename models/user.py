from models import Model
from utils import log

# class User(Model):
#     def __init__(self, form):
#         # 初始化 user，注意 若没有获取到 id 则给一个 None
#         self.id = form.get('id',None)
#         self.username = form.get('username','')
#         self.password = form.get('password','')
#         self.user_image = 'temp.jpg'
#
#
#     def salted_password(self, password, salt = '!@$#YUQLBHT'):
#         import hashlib
#         def sha256(ascii_str):
#             #加盐，hexdigest() 转化为 二进制 数据
#             return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
#         hash1 = sha256(password)
#         hash2 = sha256(hash1 + salt)
#         return hash2
#
#     def hashed_password(self,password):
#         import hashlib
#         ps = hashlib.sha256(password.encode('ascii'))
#         return ps.hexdigest()
#
#     @classmethod
#     def register(cls,form):
#         username = form.get('username','')
#         password = form.get('password','')
#         if User.find_by(username = username) is not None:
#             return False
#         elif len(username) > 2 and len(password) >5:
#             n_user = User.new(form)
#             n_user.password = n_user.salted_password(password)
#             n_user.save()
#             return n_user
#         else:
#             return None
#
#     @classmethod
#     def validate_login(cls,form):
#         name = form.get('username','')
#         psd = form.get('password','')
#         u = cls.find_by(username = name)
#         if u and u.password == u.salted_password(psd):
#             return u
#         else:
#             return None
from .mongua import Mongua
class User(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('username',str,''),
        ('password',str,''),
        ('user_image',str,''),
    ]


    def from_form(self,form):
        self.id = form.get('id',None)
        self.username = form.get('username','')
        self.password = form.get('password','')
        self.user_image = 'temp.jpg'

    def salted_password(self, password, salt = '!@$#YUQLBHT'):
        import hashlib
        def sha256(ascii_str):
            #加盐，hexdigest() 转化为 二进制 数据
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self,password):
        import hashlib
        ps = hashlib.sha256(password.encode('ascii'))
        return ps.hexdigest()

    @classmethod
    def register(cls,form):
        username = form.get('username','')
        password = form.get('password','')
        log('user_model',username,password,type(password))
        if User.find_by(username = username) is not None:
            return False
        elif len(username) > 2 and len(password) >5:
            # n_user = User.new(form)
            n_user = User.new(form)
            # n_user.from_form(form)
            n_user.username = username
            # log('n_username',u_user.username)
            n_user.password = n_user.salted_password(password)
            n_user.user_image = 'temp.jpg'
            n_user.save()
            return n_user
        else:
            return None

    @classmethod
    def validate_login(cls,form):
        # name = form.get('username','')
        # psd = form.get('password','')
        # u = cls.find_by(username = name)
        # if u and u.password == u.salted_password(psd):
        #     return u
        # else:
        #     return None
        u = User()
        u.from_form(form)
        user = User.find_by(username = u.username)
        # log('**debug',user)
        # print(user.__dict__)
        if user is not None and user.password == u.salted_password(u.password):
            log('***这一步',user.password)
            return user
        else:
            return None



