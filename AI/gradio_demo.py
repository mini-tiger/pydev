#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/09/21 15:06:38
@Author  :   zoyxiong
@File    :   gradio_demo.py
@Desc    :   gradio示例
'''


import gradio as gr

def capitalize_text(input_text):
    # 简单接口，输入转大写
    return input_text.upper()

# 输入可选组件：text, textbox, number, checkbox, dropdown, radio, image, audio, file
# 输出可选组件：text, textbox, label, image, audio, file, keyvalues, json
iface = gr.Interface(fn=capitalize_text, inputs="textbox", outputs="text")
iface.launch()