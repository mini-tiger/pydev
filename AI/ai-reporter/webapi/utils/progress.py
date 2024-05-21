import json


def progress_bar(title, last_time, used_time, rate=0):
    return f"data: {json.dumps({'title': title, 'last_time': last_time, 'used_time': used_time, 'rate': rate}, ensure_ascii=False)}"
