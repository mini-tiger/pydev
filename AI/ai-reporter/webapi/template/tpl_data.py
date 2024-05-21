


json_data_tpl = '''
{
  "Sections": [
    {
      "index": "1",
      "Section": "前言",
      "data": "%prompt",
      "proportion": "10%"
    },
    {
      "Section": "发展概述",
      "index": "2",
      "child":[
        {
          "index": "2.1",
          "Section": "战略持续拓展",
          "data": "%prompt",
          "proportion": "10%"
        },
        {
          "index": "2.2",
          "Section": "底层技术逐步成熟",
          "data": "%prompt",
          "proportion": "10%"
        }
      ]
    },
    {
      "Section": "技术发展的重要特征",
      "index": "3",
      "child": [
        {
          "index": "3.1",
          "Section": "算力融合",
          "data": "%prompt",
          "proportion": "10%"
        },
        {
          "Section": "云数融合",
          "index": "3.2",
          "data": "%prompt",
          "proportion": "10%"
        }
      ]
    },
    {
      "Section": "产业蓬勃发展",
      "index": "4",
      "data": "%prompt",
      "proportion": "10%"
    },
    {
      "Section": "数据资产化步伐稳步推进",
      "index": "5",
      "child": [
        {
          "index": "5.1",
          "Section": "数据资产管理体系仍在发展",
          "data": "%prompt",
          "proportion": "10%"
        },
        {
          "Section": "数据资产管理工具百花齐放",
          "index": "5.2",
          "data": "%prompt",
          "proportion": "10%"
        }
      ]
    }
  ]
}
'''

tpl_json_dict={"it":json_data_tpl}
