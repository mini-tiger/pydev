#-*- coding:utf-8 -*-
# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
base_dir = os.path.dirname(os.path.abspath(__file__))
# activate_this = '%s/env/bin/activate_this.py' % base_dir
# execfile(activate_this, dict(__file__=activate_this))


import sys
sys.path.insert(0, base_dir)

from bk_site import create_app
app = create_app(os.environ.get("FLASK_CONFIG") or "default")

# from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
# app = DispatcherMiddleware({'/ext': custom_app})

# log setting
import logging
import logging.config
from settings import LOGGING_DIC
logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的配置
logger = logging.getLogger(__name__)  # 生成一个log实例
logger.info('This is wsgi.py success start =========  open-falcon-dashboard')  # 记录该文件的运行状态

if __name__ == "__main__":
    app.run('0.0.0.0', 8008, debug=True)
    # app.run(host="0.0.0.0", port=8081, debug=True)
