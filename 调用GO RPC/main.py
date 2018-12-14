# coding:utf-8
import json
import socket
import itertools
import time


class RPCClient(object):
	def __init__(self, addr, codec=json):
		self._socket = socket.create_connection(addr)
		self._id_iter = itertools.count()
		self._codec = codec

	def _message(self, name, *params):
		return dict(id=self._id_iter.next(),
		            params=list(params),
		            method=name)

	def call(self, name, *params):
		req = self._message(name, *params)
		id = req.get('id')

		mesg = self._codec.dumps(req)
		self._socket.sendall(mesg)

		# This will actually have to loop if resp is bigger
		resp = self._socket.recv(4096)
		resp = self._codec.loads(resp)

		if resp.get('id') != id:  # todo 请求发送的ID,与 返回的ID一样，代表是同一个rpc连接
			raise Exception("expected id=%s, received id=%s: %s"
			                % (id, resp.get('id'), resp.get('error')))

		if resp.get('error') is not None:
			raise Exception(resp.get('error'))

		return resp.get('result')

	def close(self):
		self._socket.close()


if __name__ == '__main__':
	rpc = RPCClient(("192.168.43.26", 6038))
	mv = dict(hostname="di", version="v1", extinfo={"uuid": "abc-efg-hij"})
	print(rpc.call("Itma.UploadEnvironmentGrid", mv))  # 是falcon项目UBS itma下的方法
