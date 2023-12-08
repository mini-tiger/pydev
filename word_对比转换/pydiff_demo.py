from pydiff import DifflibParser



file1 = '''
服务方提供的妥善保管义务开始于托管服务计费开始之日，终止于计费结束之日；若在托管计费期间发生用户方设备遗失或损毁的，按照本协议第6.5条的相关约定处理。
'''

file2 = '''
服务方提供的妥善保管义务开始于之日，终止于之日；若在期间发生用户方设备遗失或损毁的，按照本协议第6.5条的相关约定处理。
'''

# with open("my.txt", 'r') as file1, open("my1.txt", 'r') as file2:
file1_content = file1.readlines()
file2_content = file2.readlines()


differ = DifflibParser(file1, file2)

for line in differ:
    print(line)
