from flask import jsonify


def page404(err):
    return jsonify({"status": 404})


def page400(err):
    return jsonify({"status": 400})


def page500(err):
    return jsonify({"status": 500})
