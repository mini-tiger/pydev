from flask import Flask, jsonify, request
from Pages.user import userbp
from Pages.admin import adminbp
import config
import errhandle
import logconfig

from functools import wraps

app = Flask(__name__)
# 异常自定义
app.register_error_handler(404, errhandle.page404)
app.register_error_handler(400, errhandle.page400)
app.register_error_handler(500, errhandle.page500)
# blueprint
app.register_blueprint(userbp)
app.register_blueprint(adminbp)


# ---------------------xxx 上下文拦截器--------------------------------------------------
@app.before_request  # 在请求收到之前绑定一个函数做一些事情。
def before_request():
    app.logger.info('before_request 本次请求路径 %s' % request.path)


@app.after_request  # 每一个请求之后绑定一个函数，如果请求没有异常。
def after_request(response):
    print('after request 返回状态', response.status)

    return response


@app.teardown_request  # 每一个请求之后绑定一个函数，即使遇到了异常。
def teardown_request(exception):
    print('teardown request path:%s,err:%s' % (request.path, exception))


# -----------------------------xxx 测试wrap页面-------------------------------------------------------


cache = dict()


def cached(timeout=5 * 60, key='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):  # 用字典 模拟 缓存，  访问过的页面，记录到缓存中
            cache_key = key % request.path  # key 是访问路径
            rv = cache.get(cache_key)
            print(rv)
            if rv is not None:
                print("使用 cached response", request.path)
                return rv
            rv = f(*args, **kwargs)
            # cache.set(cache_key, rv, timeout=timeout)
            cache.setdefault(cache_key, rv)
            return rv

        return decorated_function

    return decorator


@app.route('/', endpoint='index')
def index():
    return 'Index Page'


@app.route('/about', methods=["GET", "POST"])  # 参数获取
@cached()
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

    # 工作模式
    # gunicorn -D -w 3 main:app -b 0.0.0.0:5555
