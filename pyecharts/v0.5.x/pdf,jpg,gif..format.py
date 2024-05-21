# coding:utf-8
'''
doc:
https://github.com/pyecharts/pyecharts-snapshot

setup:
1.node.js https://nodejs.org/en/download/
2. npm install -g phantomjs-prebuilt
3.  C: > phantomjs 是否正常
3. pip install pyecharts-snapshot

phantomjs 自定义使用
https://blog.csdn.net/Lockey23/article/details/80160137
'''
from pyecharts import Bar

attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
v1 = [5, 20, 36, 10, 75, 90]
v2 = [10, 25, 8, 60, 20, 80]
bar = Bar("柱状图数据堆叠示例")
bar.add("商家A", attr, v1, is_stack=True)
bar.add("商家B", attr, v2, is_stack=True)
bar.render(path='snapshot.png', pixel_ratio=3)

# >c:\Python36\python.exe "pdf,jpg,gif..format.py"
