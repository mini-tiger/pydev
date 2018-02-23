# -*- coding:utf-8 -*-
from pykafka import KafkaClient

#kafka默认端口为9092
client = KafkaClient(hosts='kafka1:9092,kafka2:9092,kafka3:9092')#这里连接多个客户端
print client.topics
topic = client.topics['test']



message ="test message test message"
#当有了topic之后呢，可以创建一个producer,来发消息，生产kafka数据,通过字符串形式，
with topic.get_sync_producer() as producer:
	for i in range(4):
		producer.produce('test message' + str(i ** 2),partition_key='{}'.format(i))
#The example above would produce to kafka synchronously - 
#the call only returns after we have confirmation that the message made it to the cluster.
#以上的例子将产生kafka同步消息，这个调用仅仅在我们已经确认消息已经发送到集群之后

#但生产环境，为了达到高吞吐量，要采用异步的方式，通过delivery_reports =True来启用队列接口；
# with topic.get_sync_producer() as producer:
#      producer.produce('test message',partition_key='0')
# producer=topic.get_producer()
# producer.produce(message)
# print message
