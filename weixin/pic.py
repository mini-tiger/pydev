# -*- coding: utf-8 -*-

import requests
import json,time
import redis,multiprocessing

class send_pic(object):


	def Encrypt_image(self):
		data={
			"touser":"",
			"toparty":"2",
			"totay":"",
			"msgtype":"image",
			"agentid":"1",
			"image":{
				"media_id": self.media_id
			}
		}
		print data
		data=json.dumps(data,ensure_ascii=False)
		baseurl=self.baseurl="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={0}".format(self.access_token)

		hea={'Content-Type':'application/json','encoding':'utf-8'}
		req=requests.post(baseurl,data,headers=hea)
		print req.text


	def fusion_image(self,pic_file):

		files = {'file': open(pic_file, 'rb')}
		r = requests.post(self.url, files=files)
		# print r.text,type(r.text)
		self.media_id=eval(r.text)['media_id']

		self.Encrypt_image()


	def main(self,i,access_token):

		self.access_token=access_token
		self.url="https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=image" %self.access_token

		# pool=multiprocessing.Pool(processes=3)
		# for i in self.get_pic():
			# pool.apply_async(self.fusion_image,(i,))
		self.fusion_image(i)
			# self.media_id=self.upload_image(i)
			# self.Encrypt_image()
		# pool.close()
		# pool.join()

if __name__ == "__main__":
	def get_pic():
		lwzx='1.jpg'
		dti='2.jpg'
		bigdata='3.jpg'
		return [lwzx,dti,bigdata]

	def get_access_token():
		mc = redis.Redis(host='172.16.30.45', port=6379, db=0)
		token_dict = mc.get("token")
		token_dict = eval(token_dict)
		access_token= token_dict['access_token']
		return access_token


	pool=multiprocessing.Pool(processes=3)


	for i in get_pic():
		pool.apply_async(send_pic().main(i,get_access_token()))


	pool.close()
	pool.join()