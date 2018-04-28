from flask import (
    render_template,
    redirect,
    request,
    url_for,
    Blueprint
)
from utils import log
from routes import current_user
from models.board import Board

main = Blueprint('board',__name__)

@main.route('/')
def index():
    return render_template('board/board_ctrl.html')

@main.route('/add',methods = ['POST'])
def add():
    form = request.form
    log('**debug request_form',form)
    # u = current_user()
    m = Board.new(form)
    # log(m.topic_id,'m.content')
    return redirect(url_for('topic.index',page_num = 1))
