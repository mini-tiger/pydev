from flask import Flask, request, jsonify, render_template,Blueprint
import logging,json
app = Flask(__name__)


# xxx https://medium.com/@sanjan.grero/how-to-add-swagger-ui-to-a-plain-flask-api-using-an-openapi-specification-md-7ecf24976068
# swagger edit  https://editor.swagger.io/
# swagger 必须与实际服务 在一起，否则不能 try out
@app.route('/')
def get_root():
    print('sending root')
    return render_template('index.html')


@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

chat_bp = Blueprint('chat_bp', __name__)
@chat_bp.after_request  # 每一个请求之后绑定一个函数，如果请求没有异常。
def after_request_handler(response):
    args = {}
    json_data = {}
    if len(request.args.keys()) > 0:
        args = request.args

    if request.headers.get('Content-Type') == 'application/json':
        json_data = request.get_json()
    logging.info(
        'after_request 本次请求路径 %s \nrequest_params: %s \nrequest_json: %s\nresponse: %s' % (
            request.path, args, json_data, json.loads(response.data)))
    # print('after_request 本次请求路径 %s \nrequest_params: %s \nrequest_json: %s\nresponse: %s' % (
    #     request.path, args, json_data, json.loads(response.data)))
    return response
@chat_bp.route('/v1/chat', methods=["POST"])
def get_api():
    req_params = request.get_json()
    print(req_params)
    hello_dict = {'en': 'Hello', 'es': 'Hola'}
    lang = request.args.get('lang')
    return jsonify(hello_dict["en"])

from flask_cors import CORS, cross_origin

app.static_folder = "/data/work/pydev/flask-swagger/static"
app.template_folder = "/data/work/pydev/flask-swagger/template"
app.register_blueprint(chat_bp, url_prefix="/api")
CORS(app, supports_credentials=True)  # xxx 跨域
app.run(use_reloader=True, debug=False, port=8081, host="0.0.0.0")
