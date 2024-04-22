import logging
import os
import inspect
import webapi.config as config

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

        # 文件处理器 - 记录所有日志
        file_handler = logging.FileHandler(os.path.join(config.BaseConfig.base_dir,'logs' ,'all_logs.log'))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # 文件处理器 - 只记录错误及以上级别的日志
        error_file_handler = logging.FileHandler(os.path.join(config.BaseConfig.base_dir,'logs' , 'error_logs.log'))
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
