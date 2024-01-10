from datetime import datetime, timedelta, timezone
beijing = timezone(timedelta(hours=8))  #
utc_time = datetime.utcnow()  # 获取当前 UTC 时间
print(f'UTC时间为：{utc_time}')
local_time = datetime.now()  # 获取当前本地时间
print(f'本地时间为：{local_time}')

utc = timezone.utc  # 获取 UTC 的时区对象
utc_time = datetime.utcnow().replace(tzinfo=utc)  # 强制转换加上 UTC 时区。此处敲黑板，需要特别注意。
# replace的tzinfo参数为时区对象，所以
# 也可以这样 replace(tzinfo=timezone(timedelta(hours=0))
print(f'1、强制更改后的UTC时间为：{utc_time}')

time_beijing = utc_time.astimezone(beijing)
# time_newyork = utc_time.astimezone(New_York)
# time_tokyo = utc_time.astimezone(Tokyo)
print('2、更改时区为北京后的时间：', time_beijing)
print('3、获取时区信息：', time_beijing.tzinfo)
# print('4、更改时区为东京后的时间：', time_tokyo)
# print('5、获取时区信息：', time_tokyo.tzinfo)
# print('6、更改时区为纽约后的时间：', time_newyork)
