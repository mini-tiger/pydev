import logging
import os
import inspect
import config
from service.utils import create_directory_if_not_exists


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonType):
    def __init__(self):
        self.configure_logging()

    def configure_logging(self):
        # 获取当前模块的文件名
        current_file_name = inspect.getframeinfo(inspect.currentframe()).filename
        logger_name = os.path.basename(current_file_name)

        # 创建 logger
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        self.logger.setLevel(logging.INFO)

        # 创建日志格式
        formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')

        base_log_dir = os.path.join(config.BaseConfig.current_directory, 'logs')
        create_directory_if_not_exists(base_log_dir)
        # 文件处理器 - 记录所有日志
        file_handler = logging.FileHandler(os.path.join(base_log_dir, 'all_logs.log'))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # 文件处理器 - 只记录错误及以上级别的日志
        error_file_handler = logging.FileHandler(os.path.join(base_log_dir, 'error_logs.log'))
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)

        # 控制台处理器 - 打印所有日志
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # 添加处理器到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_file_handler)
        self.logger.addHandler(console_handler)


# 使用 Logger 类
logger = Logger().logger


class ContractException(Exception):
    def __init__(self, message="My custom exception"):
        self.message = message
        super().__init__(self.message)


def as_dict(obj):
    if hasattr(obj, '__table__'):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    else:
        return {}


class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)


# risk_json_record = session.query(risk_impact).filter(not_(risk_impact.match_rule_json == None)).all()
risk_json_record = []
risk_json_record_dict = [
    {'id': 2, 'important_terms': '排除我司留置权条款',
     'risk_warning': '甲方有资产托管在我司机房，甲方如逾期付款，我司享有留置权，即有权留置甲方资产通过拍卖、变卖优先受偿所得价款，以抵扣甲方欠款。如甲方在协议中排除我司留置权，则我司无权留置并处置甲方资产。',
     'examples_terms': '若甲方发生逾期支付，乙方不得留置并擅自处置甲方所有资产。', 'parts': '5.9.1.,5.9.2.,5.9.3.',
     'parts_priority': 0, 'focus': 'change,right', 'keyword': None,
     'match_rule_json': {'exclude': {'or': [], 'and': []}, 'include': {'or': ['乙方', '服务方'], 'and': ['处置']}}},
    {'id': 3, 'important_terms': '间接损失赔偿条款',
     'risk_warning': '此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。',
     'examples_terms': '乙方应赔偿甲方的全部损失，包括但不限于直接经济损失、可得收入和利润损失、商誉损失等，甲方因追究乙方违约责任而发生的包括但不限于诉讼费、律师费、公证费、保全费、公告费、鉴定费等各项费用均应由乙方承担。',
     'parts': 'xxxxxxxxx', 'parts_priority': 0, 'focus': 'left,change,right',
     'keyword': '乙方应赔偿甲方,服务方应赔偿用户方',
     'match_rule_json': {'exclude': {'or': [], 'and': []}, 'include': {'or': ['乙方', '服务方'], 'and': ['应赔偿']}}},
    {'id': 4, 'important_terms': '删除我司赔偿责任上限条款',
     'risk_warning': '如删除或修改我司赔偿责任上限条款，意味着我司对客户应承担的赔偿责任风险不可控，该赔偿责任不以我司已收取的服务费金额为赔偿上限。',
     'examples_terms': '无论何种情形下，服务方最高赔偿额不超过赔偿事项发生当月相关服务的月服务费或等额服务。',
     'parts': '2.4.,2.4节中的表格', 'parts_priority': 0, 'focus': 'left,change', 'keyword': None,
     'match_rule_json': {'exclude': {'or': [], 'and': []}, 'include': {'or': ['乙方', '服务方'], 'and': ['赔偿上限']}}},
    {'id': 7, 'important_terms': '删除设备赔偿上限条款',
     'risk_warning': '由因服务方故意或重大过失改为“因服务方原因”，造成的原因范围扩大了；其次，不仅赔偿用户方设备还需赔偿其他损失（例如数据丢失），赔偿责任加重了，且不受协议中关于赔偿上限条款的约束。整体上，提高了我司的赔偿风险。',
     'examples_terms': '服务期内因服务方故意或重大过失造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格（“封顶金额”），超过封顶金额以外的部分由用户方自行承担。     改为      服务期内因服务方原因造成用户方设备遗失或损毁的，服务方须修复、重置或赔偿，赔偿金额为所遗失或损毁的用户方设备届时重新购置的市场价格，给用户方造成其他损失的，用户方应承担赔偿责任，此赔偿责任不适用本协议第8.1条。',
     'parts': '6.5.', 'parts_priority': 0, 'focus': 'left,change', 'keyword': None,
     'match_rule_json': {'exclude': {'or': [], 'and': []}, 'include': {'or': ['乙方', '服务方'], 'and': ['封顶金额']}}},
    {'id': 8, 'important_terms': '删除用户方提前解约的违约责任',
     'risk_warning': '尤其HIT业务，此条款能有效控制我司的成本，避免损失扩大',
     'examples_terms': '用户方原因导致本合同解除、终止或本合同项下服务终止的，用户方应付清各标准服务的服务期内的剩余服务费，并应于合同解除、终止或服务终止后一个月内一次性支付予服务方。',
     'parts': '8.3.', 'parts_priority': 0, 'focus': 'left,change', 'keyword': None,
     'match_rule_json': {'exclude': {'or': [], 'and': []},
                         'include': {'or': ['甲方', '用户方'], 'and': ['剩余服务费']}}},
    {'id': 9, 'important_terms': '合作排他性条款',
     'risk_warning': '不可能因为一个公司放弃一个行业，导致我司业务发展受限。',
     'examples_terms': '合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。',
     'parts': 'xxxxxxxxx', 'parts_priority': 0, 'focus': 'left,change,right',
     'keyword': '排他性,乙方不得再与其他公司,用户方不得再与其他公司',
     'match_rule_json': {'exclude': {'or': [], 'and': []}, 'include': {'or': ['乙方', '服务方'], 'and': ['排他性']}}},
    {'id': 10, 'important_terms': '不同意转包分包条款',
     'risk_warning': '有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意。',
     'examples_terms': '用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。     改为     未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。',
     'parts': '6.6.', 'parts_priority': 0, 'focus': 'left,change', 'keyword': '分包给第三方,转包给第三方',
     'match_rule_json': {'exclude': {'or': [], 'and': []}, 'include': {'or': ['乙方', '服务方'], 'and': ['转包']}}},
    {'id': 11, 'important_terms': '保密条款只约束乙方', 'risk_warning': '保密义务是约束双方的，应改为双务条款。',
     'examples_terms': '乙方对于甲方就本协议下所交付或所知悉的任何文件、资料、机构数据及所有信息均应承担保密责任，并应负妥善保管和谨慎使用的义务。如乙方或乙方人员违反前述义务，致甲方遭受任何形式的损害或损失的，乙方及与违反保密义务的乙方人员应对甲方负连带损害赔偿责任。',
     'parts': '10.', 'parts_priority': 0, 'focus': 'left,change', 'keyword': None,
     'match_rule_json': {'exclude': {'or': [], 'and': []}, 'include': {'or': ['乙方', '服务方'], 'and': ['保密']}}},
    {'id': 12, 'important_terms': '知识产权权属', 'risk_warning': '从知识产权保护角度，应改为属于乙方。',
     'examples_terms': '本合同履行过程中，乙方在技术服务中完成的技术成果的所有权益，包括但不限于知识产权及所有权，属于甲方。',
     'parts': 'xxxxxxxxx', 'parts_priority': 0, 'focus': 'left,change,right', 'keyword': None,
     'match_rule_json': {'exclude': {'or': [], 'and': []},
                         'include': {'or': ['属于甲方', '属于用户方'], 'and': ['知识产权']}}},
]
#
# 在循环中使用这个函数
for record in risk_json_record_dict:
    risk_json_record.append(DictToObject(record))

risk_keywords_dict = {}

# risk_keyword_record = session.query(risk_impact).filter(not_(risk_impact.keyword == None)).all()
# risk_record = session.query(risk_impact).filter(risk_impact.focus.like(f'%right%'), risk_impact.parts.like(f'xx%'),
#                                                 func.length(risk_impact.keyword) > 2).all()


risk_keyword_record_dict = {'乙方应赔偿甲方': {'id': 3, 'important_terms': '间接损失赔偿条款',
                                               'risk_warning': '此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。',
                                               'examples_terms': '乙方应赔偿甲方的全部损失，包括但不限于直接经济损失、可得收入和利润损失、商誉损失等，甲方因追究乙方违约责任而发生的包括但不限于诉讼费、律师费、公证费、保全费、公告费、鉴定费等各项费用均应由乙方承担。',
                                               'parts': 'xxxxxxxxx', 'parts_priority': 0, 'focus': 'left,change,right',
                                               'keyword': '乙方应赔偿甲方,服务方应赔偿用户方',
                                               'match_rule_json': {'exclude': {'or': [], 'and': []},
                                                                   'include': {'or': ['乙方', '服务方'],
                                                                               'and': ['应赔偿']}}},
                            '服务方应赔偿用户方': {'id': 3, 'important_terms': '间接损失赔偿条款',
                                                   'risk_warning': '此损失赔偿范围太过广泛，赔偿责任过重，通常只能接受赔偿客户的直接经济损失。但如销售侧确无法删除的话，则需要在最后补充约定我司赔偿责任的上限，如合同总金额的一定百分比。',
                                                   'examples_terms': '乙方应赔偿甲方的全部损失，包括但不限于直接经济损失、可得收入和利润损失、商誉损失等，甲方因追究乙方违约责任而发生的包括但不限于诉讼费、律师费、公证费、保全费、公告费、鉴定费等各项费用均应由乙方承担。',
                                                   'parts': 'xxxxxxxxx', 'parts_priority': 0,
                                                   'focus': 'left,change,right',
                                                   'keyword': '乙方应赔偿甲方,服务方应赔偿用户方',
                                                   'match_rule_json': {'exclude': {'or': [], 'and': []},
                                                                       'include': {'or': ['乙方', '服务方'],
                                                                                   'and': ['应赔偿']}}},
                            '排他性': {'id': 9, 'important_terms': '合作排他性条款',
                                       'risk_warning': '不可能因为一个公司放弃一个行业，导致我司业务发展受限。',
                                       'examples_terms': '合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。',
                                       'parts': 'xxxxxxxxx', 'parts_priority': 0, 'focus': 'left,change,right',
                                       'keyword': '排他性,乙方不得再与其他公司,用户方不得再与其他公司',
                                       'match_rule_json': {'exclude': {'or': [], 'and': []},
                                                           'include': {'or': ['乙方', '服务方'], 'and': ['排他性']}}},
                            '乙方不得再与其他公司': {'id': 9, 'important_terms': '合作排他性条款',
                                                     'risk_warning': '不可能因为一个公司放弃一个行业，导致我司业务发展受限。',
                                                     'examples_terms': '合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。',
                                                     'parts': 'xxxxxxxxx', 'parts_priority': 0,
                                                     'focus': 'left,change,right',
                                                     'keyword': '排他性,乙方不得再与其他公司,用户方不得再与其他公司',
                                                     'match_rule_json': {'exclude': {'or': [], 'and': []},
                                                                         'include': {'or': ['乙方', '服务方'],
                                                                                     'and': ['排他性']}}},
                            '用户方不得再与其他公司': {'id': 9, 'important_terms': '合作排他性条款',
                                                       'risk_warning': '不可能因为一个公司放弃一个行业，导致我司业务发展受限。',
                                                       'examples_terms': '合作期间，乙方不得再与其他公司就与甲方经营项目服务内容相同的业务进行接洽和合作。甲、乙双方约定本协议所涉及的合作内容在同一行业内均为排他性合作。',
                                                       'parts': 'xxxxxxxxx', 'parts_priority': 0,
                                                       'focus': 'left,change,right',
                                                       'keyword': '排他性,乙方不得再与其他公司,用户方不得再与其他公司',
                                                       'match_rule_json': {'exclude': {'or': [], 'and': []},
                                                                           'include': {'or': ['乙方', '服务方'],
                                                                                       'and': ['排他性']}}},
                            '分包给第三方': {'id': 10, 'important_terms': '不同意转包分包条款',
                                             'risk_warning': '有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意。',
                                             'examples_terms': '用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。     改为     未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。',
                                             'parts': '6.6.', 'parts_priority': 0, 'focus': 'left,change',
                                             'keyword': '分包给第三方,转包给第三方',
                                             'match_rule_json': {'exclude': {'or': [], 'and': []},
                                                                 'include': {'or': ['乙方', '服务方'],
                                                                             'and': ['转包']}}},
                            '转包给第三方': {'id': 10, 'important_terms': '不同意转包分包条款',
                                             'risk_warning': '有些业务我司存在全部或部分转包分包，除非取得用户方书面同意，否则我司存在违约风险，通常很难取得用户方书面同意。',
                                             'examples_terms': '用户方同意，服务方有权将本协议项下部分或全部内容转包或者分包给第三方。     改为     未经用户方书面同意，服务方不得将本协议项下部分或全部内容转包或者分包给第三方。',
                                             'parts': '6.6.', 'parts_priority': 0, 'focus': 'left,change',
                                             'keyword': '分包给第三方,转包给第三方',
                                             'match_rule_json': {'exclude': {'or': [], 'and': []},
                                                                 'include': {'or': ['乙方', '服务方'],
                                                                             'and': ['转包']}}}}

for k, v in risk_keyword_record_dict.items():
    risk_keywords_dict[k] = DictToObject(v)
