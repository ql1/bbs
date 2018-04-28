from flask import Flask
import config

# 创建一个 flask app
app = Flask(__name__)
# 使用 flask 自带的 session， 设置 secret_key
app.secret_key = config.secret_key

# 注册蓝图，开始
from routes.index import main as index_routes
app.register_blueprint(index_routes)
from routes.topic import main as topic_routes
app.register_blueprint(topic_routes, url_prefix = '/topic')
from routes.reply import main as reply_routes
app.register_blueprint(reply_routes,url_prefix = '/reply')
from routes.board import main as board_routes
app.register_blueprint(board_routes,url_prefix = '/board')
# from routes.re
# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
