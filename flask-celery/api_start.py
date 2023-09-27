from flask import Flask, jsonify, request, make_response,g
from api.bp import create_api_bp
from flask_cors import CORS, cross_origin
from functools import wraps
import os
import time
from api import errhandle
from  api import config
from api.db import conn
from api.service import job
import celery
# celery -A make_celery worker --pool threads -l INFO

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=config.GeneralCfg.CELERY_BROKER_URL,
            result_backend=config.GeneralCfg.CELERY_RESULT_BACKEND,
            task_ignore_result=True,
        ),
    )

    app.config.from_prefixed_env()
    job.celery_init_app(app)
    return app

app = create_app()
celery_app = app.extensions["celery"]

CORS(app, supports_credentials=True)  # xxx 跨域

os.environ['CURL_CA_BUNDLE'] = ''
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# 异常自定义
app.register_error_handler(404, errhandle.page404)
app.register_error_handler(400, errhandle.page400)
app.register_error_handler(500, errhandle.page500)

create_api_bp(app)
conn.init_db(app)

# ---------------------xxx 上下文拦截器--------------------------------------------------
@app.before_request  # 在请求收到之前绑定一个函数做一些事情。
def before_request():
    request.__setattr__("reqTime", time.time())
    app.logger.info('before_request 本次请求路径 %s' % request.path)


@app.after_request  # 每一个请求之后绑定一个函数，如果请求没有异常。
def after_request(response):
    print('after request 返回状态', response.status)
    print("url:%s 用时:%.3f" % (request.path, time.time() - getattr(request, "reqTime")))

    return response


@app.teardown_request  # 每一个请求之后绑定一个函数，即使遇到了异常。
def teardown_request(exception):
    print('teardown request path:%s,err:%s' % (request.path, exception))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
    a = dict()
    val_a = os.system('df')

    a["df"] = val_a
    return a


@cross_origin()
@app.route("/uploadModel", methods=["POST"])
def uploadModel():
    file = request.files["file"]
    data = request.form.to_dict()
    name = data["Name"]
    print(name)
    print(request.headers.__str__())

    response = make_response(jsonify({"info": "模型上传成功", "status": "1"}))
    response.headers['Access-Control-Allow-Origin'] = request.headers.get("Origin")
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,DELETE,PUT,POST,PATCH,GET,TRACE,*'
    response.headers['Access-Control-Allow-Headers'] = 'content-type,*'
    response.headers['Access-Control-Max-Age'] = '3600'
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response




@app.route('/about', methods=["GET", "POST"])  # 参数获取
@cached()
def about():
    print("get args:", request.args)
    print("json args:", request.get_json())  # application/json
    print("post form args:", request.form)  # application/x-www-form-urlencoded
    print("post data args:", request.get_data())
    return jsonify({"status": config.GeneralCfg.success})


def run_flask():
    app.run(host='0.0.0.0', port=8080)
if __name__ == '__main__':
    print("url 地图:\n", app.url_map)  # 打印URL 配置

    app.config.from_object(config.DevelopmentConfig)  # 加载配置文件
    # print(app.config.items())

    # app.logger.addHandler(logconfig.info_handler)
    import multiprocessing

    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    # 可以在这里执行其他后台任务

    # 等待 Flask 进程结束（如果需要）
    # flask_process.join()


    celery_app.worker_main(argv=['worker', '--loglevel=info', '--pool=threads'])

    # app.run(host="0.0.0.0", port=8080)

    # 工作模式
    # gunicorn -D -w 3 main:app -b 0.0.0.0:5555
