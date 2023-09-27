from Question_similarity import Similarity_Score
import time, os
from api import config
from celery import shared_task, current_task
from celery.utils.log import get_task_logger
from api.db import conn

log = get_task_logger(__name__)


@shared_task(ignore_result=False)
def get_score_excel(file):
    file = os.path.basename(file)
    file_name, file_extension = os.path.splitext(file)
    # file_list = [ file_name ]
    src_dir = config.GeneralCfg.upload_qa_file_dir
    out_src_dir = config.GeneralCfg.excel_file_dir

    try:
        start = time.time()
        ss = Similarity_Score(file_prefix=file_name, run_type="text2vec", target=0.9, src_dir=src_dir,
                              out_src_dir=out_src_dir)
        ss.process()
        end = time.time()
        log.info("完成时间: %f s" % (end - start))  #
        conn.update_job_score_db(current_task.request.id, 2, time.time())
    except Exception as e:
        log.error("func get_score_excel err:%s" % e)
        conn.update_job_score_db(current_task.request.id, 3, time.time())
