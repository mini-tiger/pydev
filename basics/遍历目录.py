import os


# def Test3(rootDir, level=1):
#     if level==1:
#         print(rootDir)
#     for lists in os.listdir(rootDir):
#         path = os.path.join(rootDir, lists)
#         print('│  '*(level-1)+'│--'+lists)
#         if os.path.isdir(path):
#             Test3(path, level+1)
#
#
#
# Test3('c:\\pydev\\')

# 查找pyc文件
def Test4(rootDir, level=1):
    if level == 1:
        print(rootDir)
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)

        if os.path.isdir(path):
            print('│  ' * (level - 1) + '│--' + lists)
            Test4(path, level + 1)
        else:
            if lists.find('pyc') != -1:
                print('│  ' * (level - 1) + '│file:--' + lists)


Test4('c:\\pydev\\')
