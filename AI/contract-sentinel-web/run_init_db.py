#  pip install sqlalchemy
# pip install psycopg2
import json
import os
from typing import List

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text, PrimaryKeyConstraint, Boolean,Null
from sqlalchemy.dialects.postgresql import JSON,JSONB
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import UniqueConstraint
from service.utils import split_str
from sqlalchemy import func
from sqlalchemy import not_
from config import BaseConfig as config


# engine = create_engine(
#     f"postgresql+psycopg2://{config.PG_VCT_USER}:{config.PG_VCT_PWD}@{config.PG_VCT_HOST}:{config.PG_VCT_PORT}/{config.PG_VCT_DB}")

# if parts_priority
# else:
# # left:
# #  parts,keyword
# # right:
# #  keyword
# # change:
# #  parts,keyword
left_tpl_prefix="你是一名律师，根据你的专业知识，概括分析删除的条款对服务方或乙方有哪些影响，100字内"
change_tpl_prefix="你是一名律师，根据你的专业知识，概括分析修改的条款对服务方或乙方有哪些影响，100字内"
right_tpl_prefix="你是一名律师，根据你的专业知识，概括分析增加的条款对服务方或乙方有哪些影响，100字内"

left_tpl_user_prefix=f"{left_tpl_prefix}\n删除的条款:%s"
change_tpl_user_prefix=f"{change_tpl_prefix}\n原条款:%s修改过的条款:%s"  # #a=change_tpl_user_prefix %("abc","bcd")
right_tpl_user_prefix=f"{right_tpl_prefix}\n增加的条款:%s"


left_cot_default=f"""
{left_tpl_prefix}
示例:
  删除的条款: 不得利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动。
  AI: 风险如下:
 1. 世纪互联可能无法在法律上证明其有权禁止用户进行危害计算机信息网络安全的活动。这可能导致法律纠纷和赔偿责任。
 2. 用户信任度下降：删除此条款可能被视为世纪互联对用户安全行为的不关心，导致用户对其服务和平台产生不信任感。这可能会影响用户的忠诚度和口碑。
 3. 安全措施不足：如果删除此条款，世纪互联可能没有足够的法律依据来实施必要的安全措施，以保护其系统和用户数据免受恶意攻击。这可能导致网络安全问题和企业声誉受损。
 4. 业务拓展受限：删除此条款可能影响世纪互联与其他合作伙伴或客户签订协议的意愿，因为这可能被视为对合作伙伴或客户安全要求的忽视。
 5. 声誉受损：删除此条款可能导致公众对世纪互联的负面看法，认为其没有足够的安全措施来保护用户的网络安全。这可能会影响其业务和市场份额。
 """

left_cot_default_zhongzi=f"""
{left_tpl_prefix}
示例:
  删除的条款: 乙方应根据甲方或甲方授权的总集成单位的要求，编制或深化项目具体的验收方案，并报送甲方或总集成单位审核，经审核后的验收方案视为合同的组成部分，对乙方验收行为具有约束力。
  AI: 风险如下:
 1. 验收方案的不确定性增加。
 2. 可能意味着甲方失去了对验收方案内容的控制权，无法主动参与到方案的制定和审核过程中。这可能导致甲方对项目验收标准的需求无法得到充分体现，从而影响到项目最终的质量和结果。
 3. 甲方可能无法准确评估项目的完成情况和质量，从而增加了项目验收过程中的风险。如果项目存在问题或不符合甲方的期望，甲方可能无法有效地追究责任或要求乙方进行修正，进而导致甲方的利益受损。
 4. 没有明确的验收方案，可能会导致甲方和乙方之间对于项目完成标准的理解存在差异，进而增加合同履行过程中的沟通和纠纷。这可能会延迟项目的进展，增加双方的成本和风险。
 """

change_cot_default=f"""
示例:
  原条款: 不得利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动。
  修改过的条款: 可以利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动。
  AI: 风险如下:
 1. 世纪互联可能无法在法律上证明其有权禁止用户进行危害计算机信息网络安全的活动。这可能导致法律纠纷和赔偿责任。
 2. 用户信任度下降：修改此条款可能被视为世纪互联对用户安全行为的不关心，导致用户对其服务和平台产生不信任感。这可能会影响用户的忠诚度和口碑。
 3. 安全措施不足：如果修改此条款，世纪互联可能没有足够的法律依据来实施必要的安全措施，以保护其系统和用户数据免受恶意攻击。这可能导致网络安全问题和企业声誉受损。
 4. 业务拓展受限：修改此条款可能影响世纪互联与其他合作伙伴或客户签订协议的意愿，因为这可能被视为对合作伙伴或客户安全要求的忽视。
 5. 声誉受损：修改此条款可能导致公众对世纪互联的负面看法，认为其没有足够的安全措施来保护用户的网络安全。这可能会影响其业务和市场份额。"""

change_cot_default_zhongzi=f"""
示例:
  原条款: 如果乙方不履行合同约定的义务或其履行义务不符合合同的约定，甲方有权直接从应付乙方的任何一笔款项中扣减甲方应得之补偿。不足部分，甲方有权继续向乙方进行追偿。
  修改过的条款: 如果乙方不履行合同约定的义务或其履行义务不符合合同的约定，甲方有权继续向乙方进行追偿。
  AI: 风险如下:
 1. 甲方失去了直接从应付给乙方的款项中扣减甲方应得之补偿的权利
 2. 甲方的权利行使方式变得更加复杂，需要通过另外的追偿程序来获取补偿。
 3. 修改后的条款可能增加了甲方在实际操作中面临的不确定性和争议。
 4. 追偿程序可能会导致甲方在处理乙方违约时耗费更多时间和资源。"""


right_cot_default_zhongzi=f"""
{right_tpl_prefix}
示例:
  增加的条款: 乙方如果未近期交付，可与甲方沟通交付延后
  AI: 风险如下:
 1. 延迟交付可能导致甲方资源浪费。
 2. 交付延期可能影响甲方的业务计划。
 3. 如果合同中的延迟交付条款没有明确规定责任分担或补偿措施，那么甲方可能需要承担由于延迟交付而产生的风险和损失，而乙方则可能没有足够的激励来尽快交付。
 4. 果乙方频繁要求延期交付而没有充分的理由或者没有给出合理的解释，这可能会导致甲方对乙方的信任降低，从而影响双方未来的合作关系。
"""

right_cot_default=f"""
{right_tpl_prefix}
示例:
  增加的条款: 可以利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动。
  AI: 风险如下:
 1. 世纪互联'可能无法在法律上证明其有权禁止用户进行危害计算机信息网络安全的活动。这可能导致法律纠纷和赔偿责任。
 2. 用户信任度下降：增加此条款可能被视为世纪互联对用户安全行为的不关心，导致用户对其服务和平台产生不信任感。这可能会影响用户的忠诚度和口碑。
 3. 安全措施不足：如果增加此条款，世纪互联可能没有足够的法律依据来实施必要的安全措施，以保护其系统和用户数据免受恶意攻击。这可能导致网络安全问题和企业声誉受损。
 4. 业务拓展受限：增加此条款可能影响世纪互联与其他合作伙伴或客户签订协议的意愿，因为这可能被视为对合作伙伴或客户安全要求的忽视。
 5. 声誉受损：增加此条款可能导致公众对世纪互联的负面看法，认为其没有足够的安全措施来保护用户的网络安全。这可能会影响其业务和市场份额。
"""



match_data_list = [
    {"id": 1,
     "important_terms": "互联网信息安全责任书 网站备案义务告知书",
     "examples_terms": "IDC销售合同模板中的《互联网信息安全责任书》、《网站备案义务告知书》。",
     "risk_warning": "出处：《互联网信息服务管理办法》、《计算机信息网络国际联网安全保护管理办法》、《网络安全法》、《非经营性互联网信息服务备案管理办法》、《关于整治虚拟货币“挖矿”活动的通知》、《中华人民共和国计算机信息网络国际联网管理暂行规定》、《工业和信息化部关于清理规范互联网网络接入服务市场的通知》。",
     "left_tpl_cot":f"""
{left_tpl_prefix}
示例:
  删除的条款: 不得利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动
  AI: 风险如下:
 1. 世纪互联可能无法在法律上证明其有权禁止用户进行危害计算机信息网络安全的活动。这可能导致法律纠纷和赔偿责任。
 2. 用户信任度下降：删除此条款可能被视为世纪互联对用户安全行为的不关心，导致用户对其服务和平台产生不信任感。这可能会影响用户的忠诚度和口碑。
 3. 安全措施不足：如果删除此条款，世纪互联可能没有足够的法律依据来实施必要的安全措施，以保护其系统和用户数据免受恶意攻击。这可能导致网络安全问题和企业声誉受损。
 4. 业务拓展受限：删除此条款可能影响世纪互联与其他合作伙伴或客户签订协议的意愿，因为这可能被视为对合作伙伴或客户安全要求的忽视。
 5. 声誉受损：删除此条款可能导致公众对世纪互联的负面看法，认为其没有足够的安全措施来保护用户的网络安全。这可能会影响其业务和市场份额。
""",
     "change_tpl_cot":f"""
{change_tpl_prefix}
示例:
  原条款: 不得利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动
  修改过的条款: 可以利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动
 AI: 风险如下:
 1. 世纪互联可能无法在法律上证明其有权禁止用户进行危害计算机信息网络安全的活动。这可能导致法律纠纷和赔偿责任。
 2. 用户信任度下降：修改此条款可能被视为世纪互联对用户安全行为的不关心，导致用户对其服务和平台产生不信任感。这可能会影响用户的忠诚度和口碑。
 3. 安全措施不足：如果修改此条款，世纪互联可能没有足够的法律依据来实施必要的安全措施，以保护其系统和用户数据免受恶意攻击。这可能导致网络安全问题和企业声誉受损。
 4. 业务拓展受限：修改此条款可能影响世纪互联与其他合作伙伴或客户签订协议的意愿，因为这可能被视为对合作伙伴或客户安全要求的忽视。
 5. 声誉受损：修改此条款可能导致公众对世纪互联的负面看法，认为其没有足够的安全措施来保护用户的网络安全。这可能会影响其业务和市场份额。
""",
     "right_tpl_cot":f"""
{right_tpl_prefix}
示例:
  增加的条款: 可以利用世纪互联提供的互联网接入服务或相关业务平台从事下列危害计算机信息网络安全的活动
  AI: 风险如下:
 1. 世纪互联可能无法在法律上证明其有权禁止用户进行危害计算机信息网络安全的活动。这可能导致法律纠纷和赔偿责任。
 2. 用户信任度下降：增加此条款可能被视为世纪互联对用户安全行为的不关心，导致用户对其服务和平台产生不信任感。这可能会影响用户的忠诚度和口碑。
 3. 安全措施不足：如果增加此条款，世纪互联可能没有足够的法律依据来实施必要的安全措施，以保护其系统和用户数据免受恶意攻击。这可能导致网络安全问题和企业声誉受损。
 4. 业务拓展受限：增加此条款可能影响世纪互联与其他合作伙伴或客户签订协议的意愿，因为这可能被视为对合作伙伴或客户安全要求的忽视。
 5. 声誉受损：增加此条款可能导致公众对世纪互联的负面看法，认为其没有足够的安全措施来保护用户的网络安全。这可能会影响其业务和市场份额。
""",
     "parts": "互联网信息安全责任书,网站备案义务告知书",
     "pages": "2,3",
     "match_rule": "{}"
     },
    {"id": 2,
     "important_terms": "排除我司留置权条款",
     "examples_terms": "若甲方发生逾期支付，乙方不得留置并擅自处置甲方所有资产。",
     "risk_warning": "甲方有资产托管在我司机房，甲方如逾期付款，我司享有留置权，即有权留置甲方资产通过拍卖、变卖优先受偿所得价款，以抵扣甲方欠款。如甲方在协议中排除我司留置权，则我司无权留置并处置甲方资产。",
     "left_tpl_cot":f"""
{left_tpl_prefix}
示例:
  删除的条款: 甲方有资产托管在我司机房，甲方如逾期付款，我司享有留置权，即有权留置甲方资产通过拍卖、变卖优先受偿所得价款，以抵扣甲方欠款
  AI: 风险如下:
 1. 如甲方在协议中排除我司留置权，则乙方无权留置并处置甲方资产。
 2. 甲方违约的情况下,增加乙方回款风险
""",
     "change_tpl_cot":f"""
{change_tpl_prefix}
示例:
  原条款: 甲方有资产托管在我司机房，甲方如逾期付款，我司享有留置权，即有权留置甲方资产通过拍卖、变卖优先受偿所得价款，以抵扣甲方欠款
  修改过的条款: 甲方有资产托管在我司机房，甲方如逾期付款，乙方不得留置甲方资产
 AI: 风险如下:
 1. 如甲方在协议中排除我司留置权，则乙方无权留置并处置甲方资产。
 2. 甲方违约的情况下,增加乙方回款风险
""",
     "right_tpl_cot":f"""
{right_tpl_prefix}
示例:
  增加的条款: 甲方有资产托管在我司机房，甲方如逾期付款，乙方不得留置甲方资产
  AI: 风险如下:
 1. 如甲方在协议中排除我司留置权，则乙方无权留置并处置甲方资产。
 2. 甲方违约的情况下,增加乙方回款风险
""",
     "parts": "5.9.1,5.9.2,5.9.3",
     "pages":"",
     "focus": "change,right",
     "match_rule": "{'include':{'and':['留置'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}"
     },
    {"id": 3,
     "important_terms": "间接损失赔偿条款",
     "examples_terms": "乙方应赔偿甲方的全部损失，包括但不限于直接经济损失、可得收入和利润损失、商誉损失等，甲方因追究乙方违约责任而发生的包括但不限于诉讼费、律师费、公证费、保全费、公告费、鉴定费等各项费用均应由乙方承担。",
     "risk_warning": "此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "key_words": "乙方应赔偿甲方,服务方应赔偿用户方",
     "match_rule_json": "{'include':{'and':['应赔偿'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 无论何种情形下，服务方最高赔偿额不超过赔偿事项发生当月相关服务的月服务费或等额服务。
  AI: 风险如下:
 1. 如删除我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。
 2. 此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 无论何种情形下，服务方最高赔偿额不超过赔偿事项发生当月相关服务的月服务费或等额服务。
  修改过的条款: 乙方应赔偿甲方的全部损失，包括但不限于直接经济损失、可得收入和利润损失、商誉损失等，甲方因追究乙方违约责任而发生的包括但不限于诉讼费、律师费、公证费、保全费、公告费、鉴定费等各项费用均应由乙方承担。
 AI: 风险如下:
 1. 如删除我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。
 2. 此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款: 乙方应赔偿甲方的全部损失，包括但不限于直接经济损失、可得收入和利润损失、商誉损失等，甲方因追究乙方违约责任而发生的包括但不限于诉讼费、律师费、公证费、保全费、公告费、鉴定费等各项费用均应由乙方承担。
  AI: 风险如下:
 1. 如删除我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。
 2. 此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。
""",
     },
    {"id": 4,
     "important_terms": "删除我司赔偿责任上限条款",
     "examples_terms": "无论何种情形下，服务方最高赔偿额不超过赔偿事项发生当月相关服务的月服务费或等额服务。",
     "risk_warning": "如删除或修改我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。",
     "parts": "2.4,2.4节中的表格",
     "left_tpl_cot": f"""
 {left_tpl_prefix}
 示例:
   删除的条款: 无论何种情形下，服务方最高赔偿额不超过赔偿事项发生当月相关服务的月服务费或等额服务。
   AI: 风险如下:
  1. 如删除我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。
 """,
     "change_tpl_cot": f"""
 {change_tpl_prefix}
 示例:
   原条款: 无论何种情形下，服务方最高赔偿额不超过赔偿事项发生当月相关服务的月服务费或等额服务。
   修改过的条款: 服务方最高赔偿额不设上限
  AI: 风险如下:
 1. 如删除我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。
 """,
     "right_tpl_cot": f"""
 {right_tpl_prefix}
 示例:
   增加的条款: 无论何种情形下，服务方最高赔偿额不设上限
   AI: 风险如下:
  1. 如增加我司赔偿责任无上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。
 """,
     "match_rule_json": "{'include':{'and':['赔偿上限'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}"
     },
    {"id": 5,
     "important_terms": "删除不可抗力条款中某些事由",
     "examples_terms": "非因双方原因发生的火灾、电信网络、供电单位的电力设施故障、黑客攻击、尚无有效防御措施的计算机病毒的发作。",
     "risk_warning": "在IDC行业，发生以上事项属于我司不能预见并且对其发生和后果不能防止并避免的不可控因素，具体明确约定清楚，我司可免责。否则，我司存在违约风险。",
     "parts": "11",
     "key_words": "不可抗力",
     "left_tpl_cot": f"""
 {left_tpl_prefix}
 示例:
   删除的条款: 不可抗力中，非因双方原因发生的火灾、电信网络、供电单位的电力设施故障、黑客攻击、尚无有效防御措施的计算机病毒的发作。服务方不承担赔偿责任
   AI: 风险如下:
  1. 在IDC行业，发生以上事项属于我司不能预见并且对其发生和后果不能防止并避免的不可控因素，具体明确约定清楚，我司可免责。否则，服务方存在违约风险。
 """,
     "change_tpl_cot": f"""
 {change_tpl_prefix}
 示例:
   原条款: 不可抗力中，非因双方原因发生的火灾、电信网络、供电单位的电力设施故障、黑客攻击、尚无有效防御措施的计算机病毒的发作。服务方不承担赔偿责任
   修改过的条款: 不可抗力中，非因双方原因发生的火灾、电信网络、供电单位的电力设施故障、黑客攻击、尚无有效防御措施的计算机病毒的发作。服务方承担赔偿责任
  AI: 风险如下:
   1. 在IDC行业，发生以上事项属于我司不能预见并且对其发生和后果不能防止并避免的不可控因素，具体明确约定清楚，我司可免责。否则，服务方存在违约风险。
 """,
     "right_tpl_cot": f"""
 {right_tpl_prefix}
 示例:
   增加的条款: 不可抗力中，非因双方原因发生的火灾、电信网络、供电单位的电力设施故障、黑客攻击、尚无有效防御措施的计算机病毒的发作。服务方承担赔偿责任
   AI: 风险如下:
  1. 在IDC行业，发生以上事项属于我司不能预见并且对其发生和后果不能防止并避免的不可控因素，具体明确约定清楚，我司可免责。否则，服务方存在违约风险。
 """,
     "parts_priority": 100,
     },
    {"id": 6,
     "important_terms": "删除我司免责条款或某些事由",
     "examples_terms": "因存在下列任何一种情形，导致服务不能提供、不能及时提供或造成服务不达标的，服务方不承担责任：     9.1	用户方未依约支付费用；     9.2	自服务中断发生之时起24小时之内，用户方未向服务方书面报告的 ；     9.3	因用户方设备中的操作系统、应用程序、用户方数据以及有关的系统配置数据等的安全或管理问题而引起的；     9.4	任何用户方的电路或设备（包括用户方租用的第三方提供的设备）所引起的；     9.5	用户方的疏忽或由用户方授权服务方进行的操作所引起的；     9.6	供电单位采取的限电或断电措施；     9.7	其他由用户方原因所引起的情况。",
     "risk_warning": "主要因用户方原因，或供电单位原因导致的服务不能提供、不能及时提供或造成服务不达标的，我司免责。否则，会造成不是我司原因导致的，我司还要承担赔偿责任。",
     "parts": "2.3.2,9.1,9.2,9.3,9.4,9.5,9.6,9.7",
     "left_tpl_cot": f"""
 {left_tpl_prefix}
 示例:
   删除的条款: 因存在下列任何一种情形，导致服务不能提供、不能及时提供或造成服务不达标的，服务方不承担责任：1.	用户方未依约支付费用；2	自服务中断发生之时起24小时之内，用户方未向服务方书面报告的 ；
   AI: 风险如下:
  1. 主要因用户方原因，或供电单位原因导致的服务不能提供、不能及时提供或造成服务不达标的，服务方应该免责。
  2. 会造成不是乙方原因导致的，乙方需要承担赔偿责任。
 """,
     "change_tpl_cot": f"""
 {change_tpl_prefix}
 示例:
   原条款: 因存在下列任何一种情形，导致服务不能提供、不能及时提供或造成服务不达标的，服务方不承担责任：1.	用户方未依约支付费用；2	自服务中断发生之时起24小时之内，用户方未向服务方书面报告的 ；
   修改过的条款: 任何情况下服务不达标，服务方都需要承担赔偿责任
  AI: 风险如下:
  1. 主要因用户方原因，或供电单位原因导致的服务不能提供、不能及时提供或造成服务不达标的，服务方应该免责。
  2. 会造成不是乙方原因导致的，乙方需要承担赔偿责任的风险。
 """,
     "right_tpl_cot": f"""
 {right_tpl_prefix}
 示例:
   增加的条款:  任何情况下服务不达标，服务方都需要承担赔偿责任
   AI: 风险如下:
  1. 主要因用户方原因，或供电单位原因导致的服务不能提供、不能及时提供或造成服务不达标的，服务方应该免责。
  2. 会造成不是乙方原因导致的，乙方需要承担赔偿责任的风险。
 """,
     "parts_priority": 100,
     },
    {"id": 7,
     "important_terms": "删除设备赔偿上限条款",
     "examples_terms": "服务期内因服务方故意或重大过失造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格（“封顶金额”），超过封顶金额以外的部分由用户方自行承担。     改为      服务期内因服务方原因造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格，给用户方造成其他损失的，用户方应承担赔偿责任，此赔偿责任不适用本协议第8.1条。",
     "risk_warning": "由因服务方故意或重大过失改为“因服务方原因”，造成的原因范围扩大了；其次，不仅赔偿用户方设备还需赔偿其他损失（例如数据丢失），赔偿责任加重了，且不受协议中关于赔偿上限条款的约束。整体上，提高了我司的赔偿风险。",
     "parts": "6.5",
     "left_tpl_cot": f"""
 {left_tpl_prefix}
 示例:
   删除的条款: 服务期内因服务方故意或重大过失造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格（“封顶金额”），超过封顶金额以外的部分由用户方自行承担。
   AI: 风险如下:
  1. 由因服务方故意或重大过失改为“因服务方原因”，造成的原因范围扩大了
  2. 不仅赔偿用户方设备还需赔偿其他损失（例如数据丢失），赔偿责任加重了，且不受协议中关于赔偿上限条款的约束。
 """,
     "change_tpl_cot": f"""
 {change_tpl_prefix}
 示例:
   原条款: 服务期内因服务方故意或重大过失造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格（“封顶金额”），超过封顶金额以外的部分由用户方自行承担。
   修改过的条款: 服务期内因服务方原因造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格，给用户方造成其他损失的，用户方应承担赔偿责任，此赔偿责任不适用本协议第8.1条。"
  AI: 风险如下:
  1. 由因服务方故意或重大过失改为“因服务方原因”，造成的原因范围扩大了
  2. 不仅赔偿用户方设备还需赔偿其他损失（例如数据丢失），赔偿责任加重了，且不受协议中关于赔偿上限条款的约束。
 """,
     "right_tpl_cot": f"""
 {right_tpl_prefix}
 示例:
   增加的条款: 服务期内因服务方原因造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格，给用户方造成其他损失的，用户方应承担赔偿责任，此赔偿责任不适用本协议第8.1条。"
   AI: 风险如下:
  1. 由因服务方故意或重大过失改为“因服务方原因”，造成的原因范围扩大了
  2. 不仅赔偿用户方设备还需赔偿其他损失（例如数据丢失），赔偿责任加重了，且不受协议中关于赔偿上限条款的约束。
 """,
     "match_rule_json": "{'include':{'and':['封顶金额'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}"
     },
    {"id": 8,
     "important_terms": "删除用户方提前解约的违约责任",
     "examples_terms": "用户方原因导致本合同解除、终止或本合同项下服务终止的，用户方应付清各标准服务的服务期内的剩余服务费，并应于合同解除、终止或服务终止后一个月内一次性支付予服务方。",
     "risk_warning": "尤其HIT业务，此条款能有效控制我司的成本，避免损失扩大",
     "parts": "8.3",
     "focus": "left,change",
     "match_rule_json": "{'include':{'and':['剩余服务费'],'or':['甲方','用户方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 因用户方原因导致的服务方提前解除协议，按用户方提前终止全部服务情形处理。 服务方有权自用户方已付服务费中扣除上述服务费及违约金，不足的部分，用户方应在服务终止日后5个工作日内补足。
  AI: 风险如下:
 1. 用户方原因导致本合同解除、终止或本合同项下服务终止的，用户方应付清各标准服务的服务期内的剩余服务费，并应于合同解除、终止或服务终止后一个月内一次性支付予服务方。
 2. HIT业务，此条款能有效控制我司的成本，避免损失扩大。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 因用户方原因导致的服务方提前解除协议，按用户方提前终止全部服务情形处理。 服务方有权自用户方已付服务费中扣除上述服务费及违约金，不足的部分，用户方应在服务终止日后5个工作日内补足。
  修改过的条款: 用户方提前终止全部服务情形处理。 服务方无权自用户方已付服务费中扣除上述服务费及违约金。
 AI: 风险如下:
 1. 用户方原因导致本合同解除、终止或本合同项下服务终止的，用户方应付清各标准服务的服务期内的剩余服务费，并应于合同解除、终止或服务终止后一个月内一次性支付予服务方。
 2. HIT业务，此条款能有效控制我司的成本，避免损失扩大
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款: 用户方提前终止全部服务情形处理。 服务方无权自用户方已付服务费中扣除上述服务费及违约金。
  AI: 风险如下:
 1. 用户方原因导致本合同解除、终止或本合同项下服务终止的，用户方应付清各标准服务的服务期内的剩余服务费，并应于合同解除、终止或服务终止后一个月内一次性支付予服务方。
 2. HIT业务，此条款能有效控制我司的成本，避免损失扩大。
""",
     },
    {"id": 9,
     "important_terms": "合作排他性条款",
     "examples_terms": "合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。",
     "risk_warning": "不可能因为一个公司放弃一个行业，导致我司业务发展受限。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "key_words": "排他性,乙方不得,服务方不得",
      "match_rule_json": "{'include':{'and':['排他性'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 甲、乙双方约定本协议所涉及的合作内容在同一行业内不做为排他性合作。
  AI: 风险如下:
 1. 不可能因为一个公司放弃一个行业，导致服务方业务发展受限。
 2. IDC行业内没有这种规则
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 甲、乙双方约定本协议所涉及的合作内容在同一行业内不做为排他性合作。
  修改过的条款: 合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。
 AI: 风险如下:
 1. 不可能因为一个公司放弃一个行业，导致服务方业务发展受限。
 2. IDC行业内没有这种规则
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款: 合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。
  AI: 风险如下:
 1. 不可能因为一个公司放弃一个行业，导致服务方业务发展受限。
 2. IDC行业内没有这种规则
""",
     },
    {"id": 10,
     "important_terms": "不同意转包分包条款",
     "examples_terms": "用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。     改为     未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。",
     "risk_warning": "有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意。",
     "parts": "6.6",
     "focus": "left,change",
     "key_words": "分包给第三方,转包给第三方",
     "match_rule_json": "{'include':{'and':['转包'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。
  AI: 风险如下:
 1. 有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。
  修改过的条款: 未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。
 AI: 风险如下:
 1.  有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款: 未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。
  AI: 风险如下:
 1.  有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意。
""",
     },
    {"id": 11,
     "important_terms": "保密条款只约束乙方",
     "examples_terms": "乙方对于甲方就本协议下所交付或所知悉的任何文件、资料、机构数据及所有信息均应承担保密责任，并应负妥善保管和谨慎使用的义务。如乙方或乙方人员违反前述义务，致甲方遭受任何形式的损害或损失的，乙方及与违反保密义务的乙方人员应对甲方负连带损害赔偿责任。",
     "risk_warning": "保密义务是约束双方的，应改为双务条款。",
     "parts": "10",
     "focus": "left,change",
     "match_rule_json": "{'include':{'and':['保密'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 双方就本协议下所交付或所知悉的任何文件、资料、机构数据及所有信息均应承担保密责任，并应负妥善保管和谨慎使用的义务。
  AI: 风险如下:
 1. 保密义务是约束双方的，应改为双务条款。
 2. 保密义务是必须的，否则不符合行业标准。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 双方就本协议下所交付或所知悉的任何文件、资料、机构数据及所有信息均应承担保密责任，并应负妥善保管和谨慎使用的义务。
  修改过的条款: 乙方对于甲方就本协议下所交付或所知悉的任何文件、资料、机构数据及所有信息均应承担保密责任，并应负妥善保管和谨慎使用的义务。
 AI: 风险如下:
 1. 保密义务是约束双方的，应改为双务条款。
 2. 保密义务是必须的，否则不符合行业标准。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款: 乙方对于甲方就本协议下所交付或所知悉的任何文件、资料、机构数据及所有信息均应承担保密责任，并应负妥善保管和谨慎使用的义务。
  AI: 风险如下:
 1. 保密义务是约束双方的，应改为双务条款。
 2. 保密义务是必须的，否则不符合行业标准。
""",
     },
    {"id": 12,
     "important_terms": "知识产权权属",
     "examples_terms": "本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于甲方。",
     "risk_warning": "从知识产权保护角度，应改为属于乙方。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "match_rule_json": r"{'include':{'and':['知识产权'],'or':['属于甲方','属于用户方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于乙方。
  AI: 风险如下:
 1. 从知识产权保护角度，应改为属于乙方。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于乙方。
  修改过的条款: 本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于甲方。
 AI: 风险如下:
 1. 从知识产权保护角度，应改为属于乙方。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款:  本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于甲方。
  AI: 风险如下:
 1. 从知识产权保护角度，应改为属于乙方。
""",
     },
    {"id": 13,
     "important_terms": "关联方互不承担连带责任",
     "examples_terms": "本协议项下，甲方及其各关联公司各自承担责任，互不承担连带责任。",
     "risk_warning": "在各公司互不承担连带责任的前提下，如有个别公司未按时付款，我司则无权利向其他关联公司主张付款，增加了我司回款风险。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "match_rule_json": r"{'include':{'and':['连带责任'],'or':['甲方','用户方','关联']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 本协议项下，甲方及其各关联公司各自承担责任，承担连带责任。
  AI: 风险如下:
 1. 在各公司互不承担连带责任的前提下，如有个别公司未按时付款，我司则无权利向其他关联公司主张付款，增加了我司回款风险。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 本协议项下，甲方及其各关联公司各自承担责任，承担连带责任。
  修改过的条款: 本协议项下，甲方及其各关联公司各自承担责任，互不承担连带责任。
 AI: 风险如下:
 1. 在各公司互不承担连带责任的前提下，如有个别公司未按时付款，我司则无权利向其他关联公司主张付款，增加了我司回款风险。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款:  本协议项下，甲方及其各关联公司各自承担责任，互不承担连带责任。
  AI: 风险如下:
 1. 在各公司互不承担连带责任的前提下，如有个别公司未按时付款，我司则无权利向其他关联公司主张付款，增加了我司回款风险。
""",
     },
    {"id": 14,
     "important_terms": "违约责任不对等",
     "examples_terms": "1、乙方违反本合同约定的义务，应当向甲方支付相当于合同总金额  30 %（百分之 三十 ）的违约金。甲方则无相关约定。2、甲方逾期支付应付合同价款，经乙方书面催告后的合理期限内仍未支付的，应每日按逾期应付合同价款金额的 3 ‰（千分之 三  ）向乙方支付违约金，直至实际支付应付合同价款之日为止，甲方需支付的违约金最多不得超过逾期应付合同价款的3%（百分之 三 ）。乙方无赔偿上限约定。",
     "risk_warning": "我司违约责任过重，建议增加对等条款，或删除不利于我司的违约责任条款。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "match_rule_json": r"{'include':{'and':['无赔偿上限约定'],'or':['乙方','服务方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 乙方无赔偿上限约定。
  AI: 风险如下:
 1. 我司违约责任过重，建议增加对等条款，或删除不利于我司的违约责任条款。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 甲方逾期支付应付合同价款，经乙方书面催告后的合理期限内仍未支付的，应每日按逾期应付合同价款金额的 3 ‰（千分之 三  ）向乙方支付违约金，直至实际支付应付合同价款之日为止，甲方需支付的违约金最多不得超过逾期应付合同价款的3%（百分之 三 ）。
  修改过的条款: 甲方逾期支付应付合同价款，经乙方书面催告后的合理期限内仍未支付的，应每日按逾期应付合同价款金额的 3 ‰（千分之 三  ）向乙方支付违约金，直至实际支付应付合同价款之日为止，甲方需支付的违约金最多不得超过逾期应付合同价款的3%（百分之 三 ）。乙方无赔偿上限约定。
 AI: 风险如下:
 1. 我司违约责任过重，建议增加对等条款，或删除不利于我司的违约责任条款。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款:  甲方逾期支付应付合同价款，经乙方书面催告后的合理期限内仍未支付的，应每日按逾期应付合同价款金额的 3 ‰（千分之 三  ）向乙方支付违约金，直至实际支付应付合同价款之日为止，甲方需支付的违约金最多不得超过逾期应付合同价款的3%（百分之 三 ）。乙方无赔偿上限约定。
  AI: 风险如下:
 1. 我司违约责任过重，建议增加对等条款，或删除不利于我司的违约责任条款。
""",
     },
    {"id": 15,
     "important_terms": "知识产权许可",
     "examples_terms": "乙方保证拥有由其提供给甲方的所有产品及知识产权的合法使用权，并且已获得许可甲方使用上述产品及知识产权的正当授权并有权将产品及知识产权许可以及相关材料授权/转让给甲方。甲方可独立对本合同项下产品进行后续开发，不受知识产权限制。乙方承诺并保证甲方以非独家的、永久的、全球的、不可撤销的方式使用本合同项下标准版产品。",
     "risk_warning": "我司是否有权将产品及知识产权许可以及相关材料授权/转让给甲方？以永久的、全球的、不可撤销的方式许可甲方使用，建议慎重评估。",
     "parts": "xxxxxxxxx",
     "focus": "left,change,right",
     "match_rule_json": r"{'include':{'and':['知识产权','授权'],'or':['甲方','用户方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 服务方向用户方提供的任何资源、技术支持和服务等知识产权属于服务方所有
  AI: 风险如下:
 1. 我司是否有权将产品及知识产权许可以及相关材料授权/转让给甲方,建议慎重评估。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 服务方向用户方提供的任何资源、技术支持和服务等知识产权属于服务方所有
  修改过的条款: 乙方保证拥有由其提供给甲方的所有产品及知识产权的合法使用权，并且已获得许可甲方使用上述产品及知识产权的正当授权并有权将产品及知识产权许可以及相关材料授权/转让给甲方。甲方可独立对本合同项下产品进行后续开发，不受知识产权限制。乙方承诺并保证甲方以非独家的、永久的、全球的、不可撤销的方式使用本合同项下标准版产品。
 AI: 风险如下:
 1. 我司是否有权将产品及知识产权许可以及相关材料授权/转让给甲方？以永久的、全球的、不可撤销的方式许可甲方使用，建议慎重评估。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款:  乙方保证拥有由其提供给甲方的所有产品及知识产权的合法使用权，并且已获得许可甲方使用上述产品及知识产权的正当授权并有权将产品及知识产权许可以及相关材料授权/转让给甲方。甲方可独立对本合同项下产品进行后续开发，不受知识产权限制。乙方承诺并保证甲方以非独家的、永久的、全球的、不可撤销的方式使用本合同项下标准版产品。
  AI: 风险如下:
 1. 我司是否有权将产品及知识产权许可以及相关材料授权/转让给甲方？以永久的、全球的、不可撤销的方式许可甲方使用，建议慎重评估。
""",
     },
    {"id": 16,
     "important_terms": "争议管辖条款",
     "examples_terms": "就本合同的成立、效力和履行所发生的任何争议，双方应依据诚信原则友好协商解决。如果协商不成，双方同意将争议提交至甲方所在地法院管辖。     有客户直接约定为上海市闵行区、杭州市滨江区等所在地法院。",
     "risk_warning": "为减少诉累，建议改为原告所在地法院管辖，更为合理。或直接约定北京市朝阳区法院管辖。",
     "parts": "12",
     "focus": "left,change,right",
     "match_rule_json": r"{'include':{'and':['法院','管辖'],'or':['甲方','用户方']},'exclude':{'and':[],'or':[]}}",
     "left_tpl_cot": f"""
{left_tpl_prefix}
示例:
  删除的条款: 本协议适用中国法律，在协议执行期间如果发生争议，友好协商解决。如果协商不成，双方同意提交北京仲裁委员会仲裁解决。
  AI: 风险如下:
 1. 为减少诉累，建议改为原告所在地法院管辖，更为合理。或直接约定北京市朝阳区法院管辖。
""",
     "change_tpl_cot": f"""
{change_tpl_prefix}
示例:
  原条款: 就本合同的成立、效力和履行所发生的任何争议，双方应依据诚信原则友好协商解决。如果协商不成，双方同意将争议提交至甲方所在地法院管辖。
  修改过的条款: 就本合同的成立、效力和履行所发生的任何争议，双方应依据诚信原则友好协商解决。如果协商不成，双方同意将争议提交至上海市闵行区、杭州市滨江区等所在地法院。
 AI: 风险如下:
 1. 为减少诉累，建议改为原告所在地法院管辖，更为合理。或直接约定北京市朝阳区法院管辖。
""",
     "right_tpl_cot": f"""
{right_tpl_prefix}
示例:
  增加的条款:  就本合同的成立、效力和履行所发生的任何争议，双方应依据诚信原则友好协商解决。如果协商不成，双方同意将争议提交至上海市闵行区、杭州市滨江区等所在地法院。
  AI: 风险如下:
 1. 为减少诉累，建议改为原告所在地法院管辖，更为合理。或直接约定北京市朝阳区法院管辖。
""",
     },
]


class Base(DeclarativeBase):
    pass


word_record_risk_table = Table(
    "word_record_risk",
    Base.metadata,
    Column("word_2_record_id", ForeignKey("word_2_record.id")),
    Column("risk_impact_id", ForeignKey("risk_impact.id")),
)


class word_2_record(Base):  # 继承生成的orm基类
    __tablename__ = "word_2_record"  # 表名
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_name = Column(String(256), comment='文件名')
    line = Column(Integer, comment='row number')
    reserved = Column(Boolean, default=False, comment='是否预留')
    dyx = Column(Boolean, default=False, comment='是否深圳第一线')
    file_type = Column(String(64), comment='文件类型')
    content = Column(Text, comment='内容')
    page_number = Column(String(24), comment='页码')
    part = Column(String(64), comment='段落')
    __table_args__ = (
        UniqueConstraint('dyx', 'reserved', 'line'),
    )
    risk_impact: Mapped[List["risk_impact"]] = relationship(secondary=word_record_risk_table,
                                                            back_populates="word_2_record")


class risk_impact(Base):
    __tablename__ = "risk_impact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    important_terms: Mapped[str] = mapped_column(String(256))
    risk_warning: Mapped[str] = mapped_column(String(256))
    examples_terms: Mapped[str] = mapped_column(Text)
    parts: Mapped[str] = mapped_column(String(256))
    parts_priority = Column(Integer, default=0,comment='段落优先级')  # 设置整型字段的默认值
    focus: Mapped[str] = mapped_column(String(256))
    keyword: Mapped[str] = mapped_column(String(256),nullable=True)
    match_rule_json = Column(JSONB)
    word_2_record: Mapped[List["word_2_record"]] = relationship(secondary=word_record_risk_table,
                                                                back_populates="risk_impact")


# 创建表
# Base.metadata.create_all(engine)

# from sqlalchemy.orm import sessionmaker

# 连接到数据库
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def loadSession():
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session


# 获取数据库会话
# session = loadSession()

from service.utils import replace_str



# def insert_word2record_json_data(name, elements, record_cls):
#     add_all = []
#     query = session.query(word_2_record).filter(
#         word_2_record.file_name == name,
#         word_2_record.file_type == "docx",
#         word_2_record.reserved == record_cls.reserved,
#         word_2_record.dyx == record_cls.dyx)
#     #
#     # deleted_num = query.delete()
#     # print(f"delete row : {deleted_num}")
#     id = 0
#     max_id = session.query(func.max(word_2_record.id)).scalar()
#     if max_id is not None:
#         id = max_id
#
#     for index_offset, value in enumerate(elements):
#         index = index_offset
#         id = id + 1
#         real_txt = replace_str(value.text)
#         if len(real_txt) == 0:
#             print(f"file: {name},skip element {index}")
#             continue
#         page = record_cls.page_define(index, value)
#         part = record_cls.part_define(index, value)
#         to_create = word_2_record(
#             id=id,
#             file_name=name,
#             file_type="docx",
#             reserved=record_cls.reserved,
#             dyx=record_cls.dyx,
#             content=real_txt, part=part,
#             page_number=page, line=index)
#
#         add_all.append(to_create)
#
#     session.add_all(add_all)
#     session.commit()
#
#     print(f"insert row : {len(add_all)},elements: {len(elements)},count: {query.count()}")
#
#
# def insert_association_json_data():
#     risk_impact_data = session.query(risk_impact).all()
#     for v in risk_impact_data:
#         for subv in split_str(v.parts, ","):
#             # 不能是 like %% , 5.9.1  与 9.1类似
#             word_2_record_datas = session.query(word_2_record).filter(word_2_record.part.like(f"{subv}%")).all()
#
#             v.word_2_record.extend(word_2_record_datas)
#     session.commit()

    # d=session.query(word_2_record).filter(word_2_record.part.like(f"%网站备案义务告知书%")).first()
    # ddd = "\n".join([v.risk_warning for v in d.risk_impact])
    # print(ddd)


def to_dict(json_str):
    if json_str is not None:

        return eval(json_str)


def insert_risk_json_data(session, json_data):
    add_all = []
    for item in json_data:
        risk_impact_instance = risk_impact(
            important_terms=item.get("important_terms", ""),
            risk_warning=item.get("risk_warning", ""),
            examples_terms=item.get("examples_terms", ""),
            id=item.get("id", ""),
            parts=item.get("parts", ""),
            focus=item.get("focus", ""),
            parts_priority=item.get("parts_priority",0)
            # 如果关联关系需要建立，这里也可以处理关联关系
        )
        if "match_rule_json" in item.keys():
            match_rule_json=to_dict(item.get("match_rule_json",None))
            risk_impact_instance.match_rule_json=match_rule_json

        if "key_words" in item.keys():
            risk_impact_instance.keyword=item.get("key_words",None)

        add_all.append(risk_impact_instance)
    session.add_all(add_all)
    session.commit()




# if __name__ == "__main__":
#     # source_docx_path = "/data/work/pydev/word_对比转换/source_docx"
#     source_docx_path = config.SOURCE_DOCS_PATH
#     if config.RUN_TYPE.lower() != "product":
#         # 清空 关联 表中的数据
#         session.query(word_record_risk_table).delete()
#         # 清空 Word2Record 表中的数据
#         session.query(word_2_record).delete()
#         # 清空 risk_impact 表中的数据
#         session.query(risk_impact).delete()
#
#         # insert risk record
#         insert_risk_json_data(session, json_data=data)
#
#         file_dict = {}
#         for file in os.listdir(source_docx_path):
#             if file.endswith(".docx"):
#                 file_dict.setdefault(file, os.path.join(source_docx_path, file))
#         #
#         for name, file_path in file_dict.items():
#             print(f"=====================begin file: {name}")
#
#
#             record_cls,elements=valid_file_version(file_path)
#
#             print(f"file: {name} dyx:{record_cls.dyx} reserved:{record_cls.reserved}")
#             # insert template docx record
#             insert_word2record_json_data(name=name, elements=elements, record_cls=record_cls)
#         # insert association record
#         insert_association_json_data()
#         session.close()
