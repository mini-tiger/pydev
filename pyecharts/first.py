# coding:utf-8
# pip.exe install pyecharts
from pyecharts.charts import Bar

# bar = Bar("我的第一个图表", "这里是副标题")
# bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用

# 虚假数据
x_data = ['Apple', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo', 'Meizu']
y_data = [123, 153, 89, 107, 98, 23]


bar = (Bar()
       .add_xaxis(x_data)
       .add_yaxis('', y_data)
      )


bar.render()    # 生成本地 HTML 文件