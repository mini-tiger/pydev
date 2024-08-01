
import xml.etree.ElementTree as ET

def dict_to_xml_with_personnel(data):
    root = ET.Element("root")
    for section, members in data.items():
        section_element = ET.SubElement(root, section)
        for member in members:
            member_element = ET.SubElement(section_element, "member")
            for key, value in member.items():
                child = ET.SubElement(member_element, key)
                child.text = str(value)
    return ET.tostring(root, encoding='unicode', method='xml')

personnel_ex_str= """评估人员名单
部门负责人：
严碧波
正高级工程师
项目经理：
杜建刚
正高级工程师
项目组成员：
杨文婷
教授级高工
徐建强
研究员
专家组长
陈建林
正高级工程师
水工
杨立锋
正高级工程师
规划
钟娜
正高级工程师
总
体
廖明亮
规划水文/副总工程师
魏舫
正高级工程师
施工
万凤霞
正高级工程师
机电
傅菁菁
工程造价、施工组织设计/正高级工程师
翟洪光
正高级工程师
水库移民
徐旭敏
正高级工程师
概
算
16
"""
personnel_json= {
    "Department_Head": [
        {
            "name": "严碧波",
            "title": "正高级工程师"
        }
    ],
    "Project_Manager": [
        {
            "name": "杜建刚",
            "title": "正高级工程师"
        }
    ],
    "Project_Team_Members": [
        {
            "name": "杨文婷",
            "title": "教授级高工"
        },
        {
            "name": "徐建强",
            "title": "研究员",
            "job_titles": "专家组长"
        },
        {
            "name": "陈建林",
            "title": "正高级工程师",
            "job_titles": "水工"
        },
        {
            "name": "杨立锋",
            "title": "正高级工程师",
            "job_titles": "规划"
        },
        {
            "name": "钟娜",
            "title": "正高级工程师",
            "job_titles": "总体"
        },
        {
            "name": "廖明亮",
            "title": "副总工程师",
            "job_titles": "规划水文"
        },
        {
            "name": "魏舫",
            "title": "正高级工程师",
            "job_titles": "施工"
        },
        {
            "name": "万凤霞",
            "title": "正高级工程师",
            "job_titles": "机电"
        },
        {
            "name": "傅菁菁",
            "title": "正高级工程师",
            "job_titles": "工程造价、施工组织设计"
        },
        {
            "name": "翟洪光",
            "title": "正高级工程师",
            "job_titles": "水库移民"
        },
        {
            "name": "徐旭敏",
            "title": "正高级工程师",
            "job_titles": "概算"
        }
    ]
}

personnel_xml= dict_to_xml_with_personnel(personnel_json)
personnel_cot = """
示例:
  Human：

{ex_str}

参考示例输出，根据上面文本提取人员名单，仅xml格式化输出

  AI: {ex_xml}

""".format(ex_str=personnel_ex_str, ex_xml=personnel_xml)


project_ex_str="""中国国际工程咨询有限公司文件
咨能源[2022]2546号
中国国际工程咨询有限公司
关于青海同德抽水蓄能电站项目
（申请报告）的核准评估报告
【摘要】2021年9月国家能源局发布《抽水蓄能中长期
发展规划（2021～2035年）》，青海省共26处抽水蓄能站点纳入
中长期规划，总装机容量41700MW，同德抽水蓄能电站在内的
11处站点被列入“十四五”重点实施项目。
2022年12月，海南藏族自治州发展改革委以南发改【2022】
117号文、国家能源集团青海电力有限公司以国家能源青（2022】
283号文，分别报青海省发展改革委请求项目核准。青海省发展
改革委委托评估的重点为：项目建设必要性：项目建设规模及建
设方案：项目服务范围及电价承受能力：项目用地预审、选址意"""

project_xml="""<report>
    <year>2022</year>
    <region>青海</region>
    <reportNumber>咨能源[2022]2546号</reportNumber>
    <projectName>青海同德抽水蓄能电站项目</projectName>
    <projectField>能源</projectField>
</report>
"""

project_cot = """
示例:
  Human：

{ex_str}

从报告名称中提取 年份，报告号码，项目名称，和项目是什么领域，忽略下面的报告内容

  AI: {ex_xml}

""".format(ex_str=project_ex_str, ex_xml=project_xml)

project_human_tpl =  """

{pdf_txt}

从报告名称中提取 年份，报告号码，项目名称，和项目是什么领域，忽略下面的报告内容
"""
Project_rule = {"keywords":["中国国际工程咨询有限公司文件"],
                "pdf_page":"head_1",
                "human_tpl":project_human_tpl,
                "cot":project_cot}



Personnel_rule  = {"keywords":["评估人员名单", "咨询人员名单", "评审人员名单","审查人员名单","项目人员名单"],
                   "pdf_page":"last_5",
                   "cot":personnel_cot,
                   "human_tpl":"""
    {pdf_txt}

    参考示例输出，根据上面文本提取人员名单，仅xml格式化输出
    """}