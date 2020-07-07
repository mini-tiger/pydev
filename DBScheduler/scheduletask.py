"""
author: Bohong Xu
version: 1.0.0
description: filter the record and update the status then post the request and save the result
"""
from concurrent.futures import ThreadPoolExecutor,as_completed
import requests
import os
import json
import pprint
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import pymongo
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

mongourl = "mongodb://192.168.40.111:27017/"
max_workers = 4
dbname="petrol_data"
#set up logging for tracking
logging.basicConfig(filename='error_Log', filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.ERROR)
def execTask():
    assoclist = []
    with pymongo.MongoClient(mongourl) as myclient:

        db = myclient[dbname]
        dbcols = db['task']
        doc_count= dbcols.count_documents({"status": "1"})
        if doc_count == 0:
            return assoclist
        dbcols.update_many({"status": "1"},
        {"$set": {"status": "2"}}, upsert=False)
        res = dbcols.find({"status": "2"})

        for doc in res:
            if doc is not None:
                try:
                    checkedlist = doc["checkedlist"]
                    #checkedlist = doc["qxwjmlist"]
                    #print(checkedlist)
                    model_config = doc["model_config"]
                    #print(model_config)
                    wellname = doc["wellname"]
                    #print(wellname)
                    #print(modeldesc)
                    dict1 = {
                        "wellname": wellname,
                        "checked": checkedlist,
                        "model_config": model_config,
                    }
                    assoclist.append(dict1)

                except Exception as e:
                    pass
        return assoclist
#multithread processing the task_res
def multithreading(func, args, workers):

    with ThreadPoolExecutor(max_workers=workers) as executor:
        all_task = [executor.submit(func, arg)  for arg in args]
        for future in as_completed(all_task):
            ret = future.result()
            if not ret["success"]:
                logging.error("request and update task_res with _id {} failed".format(ret["id"]))


    print("finished")
# send the request to java restful service and update the task res
def requestExec(data ):
    headers = {
        'Content-Type' : 'application/json'
    }
    try:
        payload = {
            "data": [data["innerdata"]],
            "service": data["modeldesc"]
        }
        id = data["id"]
        packed = json.dumps(payload)
        response = requests.request("POST",
              data["modelurl"],  headers=headers, data= packed)
        ret = response.text.encode('utf8')
        with pymongo.MongoClient(mongourl) as myclient :
            db = myclient[dbname]
            dbcols = db['petrol_res']
            dbcols.update_one({"_id": id},
            {"$set": {"res": ret}}, upsert=False)
        return {"id": id, "success": True}
    except Exception as e:
        return {"id": id, "success": False}

def requestTask(assoclist):
    pprint.pprint(assoclist)
    with pymongo.MongoClient(mongourl) as myclient :
        for item in assoclist:
            jsonobj = item["model_config"]
            #pprint.pprint(jsonobj)
            modeldesc = jsonobj["model_desc"]
            modelurl = jsonobj["modelurl"]
            inparamslist  = jsonobj["inparamslist"]
            wellname = item["wellname"]
            checked = item["checked"]
            #print(modelurl)
            #print(wellname)
            #print(checked)
            #print(inparamslist)
            inpararray = inparamslist.split(",")
            #print(inpararray)

            db = myclient[dbname]
            dbcols = db['petrol_res']
            queryres = dbcols.find({"JH": wellname, "QXWJM": {'$in': checked}})

            #for elem in queryres:
            #elem = queryres.next()
            accum = []
            for elem in queryres :
                try:
                    innerdata = dict()
                    for key in inpararray:
                        innerdata[key] = str(elem[key])
                    requestbody = {
                        "id" : elem["_id"],
                        "modeldesc" : modeldesc,
                        "modelurl" : modelurl,
                        "innerdata" : innerdata
                    }
                    accum.append(requestbody)
                except Exception as e:
                   pass
                #the following code is for some sanple testing
            """
            for i in range(10):
                try:

                    innerdata ={
                        "GR" : "50.506",
                        "CAL" : "10.078",
                        "SP" : "33.799",
                        "RD" : "33.799",
                        "RS" : "33.799",
                        "CNL" : "0.001",
                        "AC" : "86.69",
                        "DRTM" : "2",
                        "SH" : "11.844",
                        "PORT" : "22.421",
                        "PORF" : "33.799", "PERM" : "190.1320038",
                        "DRES" : "33.799",
                        "LOGRD" : "0.788",
                        "LOGRS" : "0.401",
                        "LOGDRES" : "0.605",
                        "DCAL" : "0.401",
                        "DAC" : "0.605"
                    }
                    requestbody = {
                        "id": elem["_id"],
                        "modeldesc": modeldesc,
                        "modelurl": modelurl,
                        "innerdata": innerdata
                    }
                    #pprint.pprint(requestbody)
                    accum.append(requestbody)
                except Exception as e:
                   pass
            """
            multithreading(requestExec, accum, max_workers)
#update the status and make the task_res for next step
def finishJob():
    with pymongo.MongoClient(mongourl) as myclient:
        db = myclient[dbname]
        dbcols = db['task']
        dbcols.update_many({"status": "2"},
        {"$set": {"status": "3"}}, upsert=False)
def wholeprocess():
    preparedTask = execTask()
    if(len(preparedTask) > 0):
        requestTask(preparedTask)
        finishJob()
if __name__ == '__main__':
    logger = logging.getLogger('error_log')
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    #the timed schedulter with apscheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(wholeprocess, 'interval', minutes=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    #scheduler = BlockingScheduler(jobstores=jobstores)
    #scheduler.configure(timezone='Asia/Kolkata')
    #scheduler.add_jobstore('mongodb', collection='example_jobs')

