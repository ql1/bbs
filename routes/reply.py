from flask import (
    render_template,
    redirect,
    request,
    url_for,
    Blueprint
)
from utils import log
from routes import current_user
from models.reply import Reply

main = Blueprint('reply',__name__)

@main.route('/add',methods = ['POST'])
def add():
    form = request.form
    u = current_user()
    m = Reply.new(form)
    m.set_user_id(u.id)
    log(m.topic_id,'m.content')
    return redirect(url_for('topic.detail',id = m.topic_id))
