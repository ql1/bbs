from flask import (
    render_template,
    redirect,
    request,
    url_for,
    Blueprint
)
from utils import log
from routes import *
from models.topic import Topic
from models.board import Board
from utils import translate_time


# def time_sort(x,y):
#     if x.update_time < y.update_time:
#         return 1
#     elif x.update_time > y.update_time:
#         return -1
#     else:
#         return 0
#下面函数求取页码对应的topic
# def page_count(page = 1):
# 	ms = topic.all()
# 	ms.sort()
# 	#sort方法已有 通过发布时间排序
# 	ms[40 * (page -1) : 40 * page]

main = Blueprint('topic',__name__)

@main.route('/<int:page_num>')
def index(page_num = 1):
    board_id = int(request.args.get('board_id',-1))
    #如果是-1 就是没有 也就是全部Topic
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()
    ms.sort(key=lambda x:x.update_time,reverse=True)

    # ms  即查出的所有需要传入模板的topic
    ms = ms[10 * (page_num -1) : 10 * page_num]
    for m in ms:
        # log('**ms debug',ms)
        m.post_time = translate_time(m.update_time)
    # 在后端计算出需要几页，赋值给 page_all 变量 传给前端
    print(len(ms))
    page_all = (int(len(ms)/10)) + 1
    user = current_user()
    return render_template('topic/index.html',ms = ms,bs = bs,user = user.username,page_all = page_all,currentpage=page_num)

@main.route('/topic_list/<int:id>')
def detail(id):
    m = Topic.get(id)
    # some_day = time.time
    m.post_time = translate_time(m.update_time)
    user_id = m.user_id
    u = User.find_by(id = user_id)
    author = u.username
    b = Board.find(m.board_id)
    place = b.title
    return render_template('topic/detail.html',topic = m,author = author,place = place)

@main.route('/add',methods = ['POST'])
def add():
    u = current_user()
    form = request.form
    log('form,************09',form)
    m = Topic.new(form,user_id = u.id)
    return redirect(url_for('index.index'))

@main.route('/new')
def new():
    bs = Board.all()
    log('**debug Board',bs)
    return render_template('topic/new.html',bs = bs)

