from flask import Flask, url_for, jsonify, request
from user import userbp
from admin import adminbp
import config
import errhandle

app = Flask(__name__)
# 异常自定义
app.register_error_handler(404, errhandle.page404)
app.register_error_handler(400, errhandle.page400)
app.register_error_handler(500, errhandle.page500)
# blueprint
app.register_blueprint(userbp)
app.register_blueprint(adminbp)


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
    app.run(host="0.0.0.0", port=5555)
