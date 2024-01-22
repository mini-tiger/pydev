# coding=utf-8
from __future__ import unicode_literals
# 地图安装包
# pip install echarts-countries-pypkg
# pip install echarts-china-provinces-pypkg
# pip install echarts-china-cities-pypkg
# pip install echarts-china-counties-pypkg
# pip install echarts-china-misc-pypkg
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

    # show label
value = [155, 10, 66, 78]
attr = ["福建", "山东", "北京", "上海"]
map = Map("全国地图示例", width=1200, height=800)
map.add("", attr, value, maptype="china", is_label_show=True,
        is_visualmap=True, visual_text_color='#000')
map.on(events.MOUSE_CLICK, on_click)
map.render(r'map.html')
# content = get_default_rendering_file_content()
# assert "function on_click(params) {" in content
# assert '("click", on_click);' in content
