运行fastapi_demo
locust -f demo_locust_压力.py --headless -u 100 -r 100 -t 1m --html locust_report.html
 
-f locust_test.py //代表执行哪一个压测脚本
--headless //代表无界面执行
-u 100 //模拟100个用户操作
-r 100 //每秒用户增长数
-t 10m //压测10分钟
--html report.html //html结果输出的文件路径名称,无需提前创建，自动生成