#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
https://github.com/hiyouga/LLaMA-Factory/blob/v0.3.3/src/web_demo.py
'''


import gradio as gr

def capitalize_text(input_text):
    # 简单接口，输入转大写
    return input_text.upper()

# 输入可选组件：text, textbox, number, checkbox, dropdown, radio, image, audio, file
# 输出可选组件：text, textbox, label, image, audio, file, keyvalues, json
iface = gr.Interface(fn=capitalize_text, inputs="textbox", outputs="text")
iface.launch()