from flask import Blueprint, jsonify

adminbp = Blueprint('adminbp', __name__, url_prefix='/admin')


@adminbp.route('/')
def index():
    return 'Admin blueprint, index page'


@adminbp.route('/json')
def json():
    return jsonify({"a": 1})
