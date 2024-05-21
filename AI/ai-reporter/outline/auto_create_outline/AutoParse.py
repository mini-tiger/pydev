import re
import json
from outline.util.UtilTools import UtilTools

class AutoParse():

    def parse2Json(self,subject,content_list,total_num):
        tools = UtilTools()

        zhang = 0
        dagang = {"title":"","Sections":[]}
        ispass = False
        zhang_list = []
        dagang["title"] = subject
        bar_num = 0
        for pl in  content_list:
            list = []
            pls = pl.split('\n')
            for p in pls:
                list.append(p)
            jie = 0
            biaohao_num = 0
            biaohao_num_tag = False
            for paragraph in list:
                paragraph_line = paragraph.strip()
                paragraphs =  paragraph_line.split(" ")
                
                #if len(paragraphs) != 2:
                #
                if len(paragraphs) < 2:
                    continue
                if ispass:
                    continue

                
                #解析结束符
                if biaohao_num_tag and biaohao_num > 0:
                    break
                if '---' in paragraph_line:
                    #break
                    biaohao_num += 1
                if '总结格式' in paragraph_line:
                    break
                if '例如' in paragraph_line:
                    break
                if '每个章节' in paragraph_line:
                    break
                if '第N章' in paragraph_line:
                    break
                if '第N节' in paragraph_line:
                    break
                if '请注意' in paragraph_line:
                    break
                if zhang >= total_num and jie >=3:
                    break
                

                #解析出章的内容
                # a 第一章 引言 b 第1章 引言 c 1. 引言
                if re.match("^(第)[\u4e00-\u9fa5]+(章)$",paragraphs[0]) or re.match("^(第)[0-9]+(章)$",paragraphs[0]) or re.match("^[0-9]+\\.\\s[\u4e00-\u9fa5]+$",paragraph_line):
                    if paragraphs[1] in zhang_list:
                        ispass = True
                        continue
                    zhang = zhang + 1 
                    jie = 0
                    zhang_num = tools.digit_to_chinese(zhang)
                    if "一十" in zhang_num:
                        zhang_num = zhang_num.replace("一十","十")
                    zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  paragraphs[1],"child":[]}
                    dagang["Sections"].append(zhang_section)
                    zhang_list.append(paragraphs[1])
                    ispass = False
                    biaohao_num_tag = True
                # d 1. 第一章 引言 b 1. 第1章 引言
                elif re.match("^[0-9]+\\.\\s(第)[\u4e00-\u9fa5]+(章)$",paragraphs[0] + " " + paragraphs[1]) or re.match("^[0-9]+\\.\\s(第)[0-9]+(章)$",paragraphs[0] + " " + paragraphs[1]):
                    if paragraphs[1] in zhang_list:
                        ispass = True
                        continue
                    zhang = zhang + 1 
                    jie = 0
                    zhang_num = tools.digit_to_chinese(zhang)
                    if "一十" in zhang_num:
                        zhang_num = zhang_num.replace("一十","十")
                    zhang_section = {"index": zhang,"Section": "第" + zhang_num + "章 " +  paragraphs[2],"child":[]}
                    dagang["Sections"].append(zhang_section)
                    zhang_list.append(paragraphs[1])
                    ispass = False
                    biaohao_num_tag = True

                #解析出每小节的内容
                # a 第一节 研究背景及意义 b 第1节 研究背景及意义
                elif re.match("^(第)[\u4e00-\u9fa5]+(节)$",paragraphs[0]) or re.match("^(第)[0-9]+(节)$",paragraphs[0]) :
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  paragraphs[1]}
                    dagang["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num += 1
                # c 1. 第一节 研究背景及意义 d 1. 第1节 研究背景及意义 e - 第一节 研究背景及意义 f - 第1节 研究背景及意义
                elif re.match("^[0-9]+\\.\\s(第)[\u4e00-\u9fa5]+(节)$",paragraphs[0] + " " + paragraphs[1]) or re.match("^[0-9]+\\.\\s(第)[0-9]+(节)$",paragraphs[0] + " " + paragraphs[1]) or re.match("^-\\s(第)[\u4e00-\u9fa5]+(节)$",paragraphs[0] + " " + paragraphs[1]) or re.match("^-\\s(第)[0-9]+(节)$",paragraphs[0] + " " + paragraphs[1]):
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  paragraphs[2]}
                    dagang["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num += 1
                # g - 研究背景及意义
                elif re.match("^-\\s[\u4e00-\u9fa5]+$",paragraphs[0] + " " + paragraphs[1]):    #
                    jie = jie + 1
                    jie_num = tools.digit_to_chinese(jie)
                    if "一十" in jie_num:
                        jie_num = jie_num.replace("一十","十")
                    jie_section = {"index": jie,"Section": "第" + jie_num + "节 " +  paragraphs[1]}
                    dagang["Sections"][zhang-1]["child"].append(jie_section)
                    bar_num += 1
                else:
                    continue
            
            avg = str(round(round(1 / bar_num, 3) * 100,1)) + "%"
            for i in range(len(dagang["Sections"])):
                for j in range(len(dagang["Sections"][i]["child"])):
                    dagang["Sections"][i]["child"][j]["proportion"] = avg
                    dagang["Sections"][i]["child"][j]["data"] = ""
        #print(json.dumps(dagang, indent=4, ensure_ascii=False))
        return dagang,bar_num

    def digit_to_chinese(self,num):
        digit_list = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        unit_list = ['', '十', '百', '千', '万']
        
        if num < 0:
            return "请输入非负整数"
        if num < 10:
            return digit_list[num]
        
        result = ''
        num_str = str(num)
        length = len(num_str)
        for i, digit in enumerate(num_str):
            digit = int(digit)
            if digit != 0:
                result += digit_list[digit] + unit_list[length - i - 1]
            else:
                if i < length - 1 and int(num_str[i + 1]) != 0:
                    result += digit_list[digit]
        return result