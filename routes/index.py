from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import send_from_directory
import json

from config import user_file_d

from utils import log

from models.user import User


def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u

def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type as allow_type
    return suffix in allow_type

main = Blueprint('index', __name__)


@main.route('/')
def index():
    # # return 'helloword'
    # u = current_user()
    # log(u)
    # if u is None:
    #     return redirect(url_for('topic.index'))
    # else:
    u = current_user()
    log('who is u', u)
    if u is not None:
        # log('who2')
        # if u.user_image == None:
        #     u.user_image = 'temp.jpg'
        return redirect(url_for('topic.index',page_num = 1))
    # log('who')

    return render_template('index.html')

# register
@main.route('/register_p')
def register_p():
    return render_template('register_p.html')

@main.route('/login_P')
def login_p():
    return render_template('login_p.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form

    form = form.to_dict()
    for k,v in form.items():
        temp = k
    form = json.loads(temp)
    log('form',form,type(form))
    # for i in form:
    #     log(i)
    # log('register-form',form,type(form))
    # # form = dict(form)
    # log('finally-form',form,type(form))
    u = User.register(form)
    message = 0
    #message 即返回给ajax 的状态，-1为重名，1为正常，0为其他 用户名长度问题
    if u == False:
        message = -1
    elif u.__class__.__name__ == 'User':
        message = 1
    else:
        message = 0
    log('message',message)
    message = json.dumps(message)
    return message


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    log('login',form)
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        log(type(u))
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index',page_num = 1))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)




@main.route('/adding',methods=['POST',])
def add_img():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if allow_file(file.filename):
        from werkzeug import secure_filename
        filename = secure_filename(file.filename)
        import os

        file.save(os.path.join(user_file_d, filename))
        u.user_image = filename
        u.save()
    return redirect(url_for('.profile'))

@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(user_file_d, filename)

@main.route('/logout')
def logout():
    # u = current_user()
    session.pop('user_id')
    return redirect(url_for('.index'))

# @main.route('/<int:id>')
@main.route('/profile/<int:user_id>')
def user_profile(user_id):
    u = User.find(user_id)
    return render_template('user_profile.html',u = u)
    # render_template()
    # if u is None:
    #     return redirect(url_for('.index'))
    # else:
    #     return render_template('profile.html', user=u)


