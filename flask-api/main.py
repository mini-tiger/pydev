from flask import Flask, jsonify, request
from Pages.user import userbp
from Pages.admin import adminbp
import config
import errhandle
import logconfig

app = Flask(__name__)
# 异常自定义
app.register_error_handler(404, errhandle.page404)
app.register_error_handler(400, errhandle.page400)
app.register_error_handler(500, errhandle.page500)
# blueprint
app.register_blueprint(userbp)
app.register_blueprint(adminbp)


@app.before_request  # 在请求收到之前绑定一个函数做一些事情。
def before_request():
    print('before_request 本次请求路径', request.path)


@app.after_request  # 每一个请求之后绑定一个函数，如果请求没有异常。
def after_request(response):
    print('after request 返回状态', response.status)
    return response


@app.teardown_request  # 每一个请求之后绑定一个函数，即使遇到了异常。
def teardown_request(exception):
    print('teardown request path:%s,err:%s' % (request.path, exception))


# ------------------------------------------------------------------------------------

@app.route('/', endpoint='index')
def index():
    return 'Index Page'


@app.route('/about', methods=["GET", "POST"])  # 参数获取
def about():
    print("get args:", request.args)
    print("json args:", request.get_json())  # application/json
    print("post form args:", request.form)  # application/x-www-form-urlencoded
    print("post data args:", request.get_data())
    return jsonify({"status": config.GeneralCfg.success})


if __name__ == '__main__':
    print("url 地图:\n", app.url_map)  # 打印URL 配置

    app.config.from_object(config.DevelopmentConfig)  # 加载配置文件
    # print(app.config.items())

    app.logger.addHandler(logconfig.info_handler)

    app.run(host="0.0.0.0", port=5555)
