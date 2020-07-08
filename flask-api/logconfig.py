import logging
from logging.handlers import TimedRotatingFileHandler

# 单文件
# handler = logging.FileHandler('/home/pydev/flask-api/flask.log', encoding='UTF-8')
# handler.setLevel(logging.DEBUG)
# logging_format = logging.Formatter(
#     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
# handler.setFormatter(logging_format)

# 每天分割
logger = logging.getLogger('flask_logger')
# 设置日志基础级别
logger.setLevel(logging.DEBUG)
# 日志格式
formatter = '%(asctime)s: %(levelname)s %(filename)s-%(module)s-%(funcName)s-%(lineno)d %(message)s'
log_formatter = logging.Formatter(formatter)
# info日志处理器
info_handler = TimedRotatingFileHandler(filename='info.log', when='D', interval=1, backupCount=7, encoding='utf-8')
# log_handler.suffix = '%Y-%m-%d.log'
# log_handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
info_handler.setFormatter(log_formatter)
# 错误日志处理器
# err_handler = TimedRotatingFileHandler(filename='error.log', when='D', interval=1, backupCount=7, encoding='utf-8')
# err_handler.suffix = '%Y-%m-%d.log'
# err_handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}.log')
# err_handler.setFormatter(log_formatter)

# 添加日志处理器
# logger.addHandler(info_handler)
# logger.addHandler(err_handler)