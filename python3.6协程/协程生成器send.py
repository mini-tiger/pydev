# 在并发高，连接活跃度不高的情况下，Epoll 比Select 好
# 在并发不高，连接活跃度高的情况 下，select 比epool 好

# import socket
# from urllib.parse import urlparse
# from selectors import DefaultSelector  # linux 自动是epool windows 是 Select
# from selectors import EVENT_READ, EVENT_WRITE
#
# selector = DefaultSelector
#
#
# class Fetcher:
#
#     def connected(self, key):
#         selector.unregister(key.fd)  # 消除注册刚才的 文件描述符
#         self.client.send("GET / HTTP/1.1\r\n".encode("utf-8"))  # 发送文字
#
#         selector.register(self.client.fileno(), EVENT_READ, self.readable)  # 重新注册 接收数据的 事件
#
#     def readable(self, key):
#
#         d = self.client.recv(1024)
#         if d:
#             self.data += d
#         else:
#             selector.unregister(key.fd)
#         data = self.data.decode("utf-8")
#         html_data = data.split("\r\n\r\n")[1]
#         print(html_data)
#         self.client.close()
#
#     def get_url(self, url):
#         url = urlparse(url)
#         self.host = url.netloc
#         self.path = url.path
#         self.data = b""
#         if self.path == "":
#             self.path = "/"
#
#         # 建立socketl连接
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.client.setblocking(False)
#
#         try:
#             self.client.connect((self.host, 80))
#         except BlockingIOError as e:
#             pass
#
#         # 注册事件, 连接的文件描述符, 事件的种类（写数据）,回调函数
#
#         selector.register(self.client.fileno(), EVENT_WRITE, self.connected)
#
#
# def loop():
#     # 事件循环，不停的请求SOCKET 并调用 对应的回调函数
#     while True:
#         ready = selector.select()
#         for key, mask in ready:
#             call_back = key.data
#             call_back(key)
#     # 回调+ 事件循环 + select(pool/epool)
#
#
# if __name__ == "__main__":
#     fetcher = Fetcher()
#     fetcher.get_url("http://www.baidu.com")
#     loop()

import random, time


def genNum(n):
    for i in range(0, n):
        n = yield random.randint(0, 10)  # 使用send方法，这里每次都会被覆盖
        print(n)
        m = yield 2
        print(m)
        print("this is random int", n, m, i, m * n * i)


if __name__ == "__main__":
    g = genNum(5)
    next(g)  # todo 第一次启动生成器必须要用next()或者 g.send(None)

    while True:
        try:
            g.send(1)
            g.send(3) # 如果有两个yield ，需要用两个send
        except StopIteration as e:
            break
# todo 每个yield 返回的n 都被send(1) 中的 1 替换
# this is random int 1 3 0 0
# this is random int 1 3 1 3
# this is random int 1 3 2 6
# this is random int 1 3 3 9
# this is random int 1 3 4 12
