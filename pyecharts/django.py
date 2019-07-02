# coding=utf-8
from __future__ import unicode_literals
import math
# from django.http import HttpResponse
from jinja2 import Environment, PackageLoader

#
# print template.render(abc='variables', aaa='here')

from pyecharts import Map
import pyecharts.echarts.events as events
from pyecharts_javascripthon.dom import alert
import pyecharts

pyecharts.configure(
    jshost=None,
    echarts_template_dir=None,
    force_js_embed=None,
    output_image=None,
    global_theme=None
)


def on_click(params):
    alert(params.name)




REMOTE_HOST = "https://pyecharts.github.io/assets/js"

import os
# print os.getcwd()
def index():
    env = Environment(loader=PackageLoader(package_name='template', package_path='.'))
    template = env.get_template('pyecharts.html')
    l3d = map()
    # show label


    context = dict(
        myechart=l3d.render_embed(), # 图片
        host=REMOTE_HOST,
        script_list=l3d.get_js_dependencies() # js依赖包
    )
    with open("lin3d.html","w+") as f:
        f.write(template.render(context))


def map():
    value = [155, 10, 66, 78]
    attr = ["福建", "山东", "北京", "上海"]
    map = Map("全国地图示例", width=1200, height=800)
    map.add("", attr, value, maptype="china", is_label_show=True,
            is_visualmap=True, visual_text_color='#000')
    map.on(events.MOUSE_CLICK, on_click)
    # map.render(r'map.html')
    return map

if __name__ == "__main__":
    index()