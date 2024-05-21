from outline.CreateOutline import CreateOutline
from outline.auto_create_outline.AutoCreateOutline import AutoCreateOutline
from outline.auto_create_outline.UseAdapterCreateOutline import UseAdapterCreateOutline
from outline.auto_create_outline.UseJsonCreateOutline import UseJsonCreateOutline
import re
import json
from outline.util.UtilTools import UtilTools
import openai
#from flask import Flask,jsonify


#中国星球大战发展趋势报告
#中国农耕社会发展趋势报告
#中国历史研究报告 中国历史研究报告
'''
u = UseAdapterCreateOutline()
#d = u.create_half_template("麻黄病的研究",5,"http://120.133.63.162:33382/v1/")
d = u.createOutline("乙酸乙酯研究报告",5,"http://120.133.63.162:33382/v1/")
#u.parse_outline("python整除",d)
'''

'''
u = UseJsonCreateOutline()
#d = u.createOutline("我的小猫运势",5,"http://120.133.83.145:8000/v1/")
d = u.createOutline("我的小猫运势",5,"http://120.133.63.166:8002/v1/")
u.parseAndCreateJson("我的小猫运势",d)
'''

c = CreateOutline()
c.create_outline("中国历史研究报告","","智能生成","50000","http://120.133.63.162:33383/v1/")


'''

d = """
好的，我将根据您的要求生成大纲。以下是大纲：

章节：远程医疗行业概述
1. 小节：远程医疗的定义和发展历程
2. 小节：远程医疗的分类和应用领域
3. 小节：远程医疗的优势和挑战

章节：远程医疗技术的发展
1. 小节：远程医疗技术的发展历程
2. 小节：远程医疗技术的种类和特点
3. 小节：远程医疗技术的应用和影响

章节：远程医疗的市场现状
1. 小节：远程医疗市场的规模和增长趋势
2. 小节：远程医疗市场的竞争格局和主要参与者
3. 小节：远程医疗市场的机遇和挑战

章节：远程医疗的政策环境
1. 小节：远程医疗的政策背景和法规框架
2. 小节：远程医疗的政策支持和鼓励措施
3. 小节：远程医疗的政策挑战和应对策略

章节：远程医疗的未来发展趋势
1. 小节：远程医疗的未来发展趋势和预测
2. 小节：远程医疗的未来挑战和应对策略
3. 小节：远程医疗的未来机遇和前景

请把上面的大纲以json的格式输出
"""
'''




'''
for i in range(20):
    c = CreateOutline()
    outline = c.create_outline("全球数字治理白皮书","数字治理","测试治理",10000,"http://120.133.63.166:8006/v1/")
    print(json.dumps(outline, indent=4, ensure_ascii=False))
    #print(outline)

'''
'''
c = CreateOutline()
outline = c.create_outline("全球数字治理白皮书","数字治理","智能生成




10000,"")
print(json.dumps(outline, indent=4, ensure_ascii=False))
'''
'''
openai.api_key = "Empty"http://120.133.75.252:28006/v1/
openai.base_url = "http://120.133.63.162:33383/v1/"
completion = openai.chat.completions.create(
    model="Baichuan2-13B-Chat",
    messages=[
        #{"role": "user", "content": "你是中文文档编写助手\n\n当前阶段是用中文编写大纲，你将根据报告主题创建大纲，你的决策将独立执行而不依赖于人类的帮助，请发挥LLM的优势并且追求高效的策略进行输出大纲。报告主题: 今年是2024年,报告主题为中国自行车发展现状\n根据提供的报告主题,生成10个章节,每个章节至少有3个小节;大纲只细分到小节,每个小节下面不要再生成内容;你只能以以下json列表的格式生成大纲[{\"ct\":\"章节1标题\",\"ci\":1,\"Section\":[{\"si\":1,\"st\":\"小节1标题\"},{\"si\":2,\"st\":\"小节2标题\"},{\"si\":3,\"st\":\"小节3标题\"}]}]\n确保Task可以被Python的json.loads解析"},
        {"role": "user", "content": d},
    ],
    max_tokens=4000, 
    n=1,  # 设置生成的选项数量为1
    stop=None,  # 不设置停止条件
    temperature=0,  # 设置温度为0.5，
    timeout=300,
)
content = completion.choices[0].message.content
print(content)
'''
'''
#c.checkKeyWord("中国美的电饭锅产业研究报告")
#c.getReportType()
#c.checkReportType("中国美的电饭锅产业研究报告")

#a = AutoCreateOutline()
#list = a.createOutline("中国美的电饭锅产业研究报告")
#print(list)
'''


