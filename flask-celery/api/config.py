import os
from api import tools
class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    TESTING = False
    DB_SERVER = '192.168.1.56'

    @property
    def DATABASE_URI(self):  # Note: all caps
        return 'mysql://user@{}/foo'.format(self.DB_SERVER)


class ProductionConfig(Config):
    """Uses production database server."""
    DB_SERVER = '192.168.19.32'


class DevelopmentConfig(Config):
    DB_SERVER = 'localhost'
    # SERVER_NAME = '192.168.43.26:5555'
    DEBUG = True


class TestingConfig(Config):
    DB_SERVER = 'localhost'
    DEBUG = True
    DATABASE_URI = 'sqlite:///:memory:'


class GeneralCfg(object):
    success = 200
    fail = 400
    current_directory = os.path.dirname(__file__)

    # upload_qa_file_dir = "/mnt/AI_Json/re"
    excel_file_dir = os.path.join(current_directory,"file_store","excelfile")

    upload_qa_file_dir = os.path.join(current_directory,"file_store","uploadfile")
    tools.mkdir(excel_file_dir)
    tools.mkdir(upload_qa_file_dir)
    print(excel_file_dir)
    print()
    CELERY_BROKER_URL = 'redis://:cc@172.22.50.25:32679/7'
    CELERY_RESULT_BACKEND = 'redis://:cc@172.22.50.25:32679/7'

    def __init__(self):
        pass
    #
    # @property
    # def success(self):
    #     return 200
    #
    # @property
    # def fail(self):
    #     return 400
