import pymongo
from bson.objectid import ObjectId

mongoclient = pymongo.MongoClient('mongodb://auto:auto@192.168.40.124:27017')
db = mongoclient["server_auto"] # 数据库名字



def fetchAll(collction:str,filter:dict):
    Cursor = db[collction]

    # for x in collection.find(filter, {"_id": 0}):
    #     print(x)

    # return list(Cursor.find(filter, {"_id": 0})) #todo  _id字段 不能Jsonable_encoder

    l=list()
    for i in Cursor.find(filter):
        i["_id"]=i["_id"].__str__()
        l.append(i)
    return l



def fectchOne(collction:str,id:str):
    Cursor = db[collction]
    return Cursor.find_one({'_id':ObjectId(id)})