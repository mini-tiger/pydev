import os,re

def add_enter(my_string):
    # 检查字符串开头是否有回车
    if my_string.startswith("\n") == False :
        # 在字符串开头添加回车
        my_string = "\r\n" + my_string
        # print("已添加回车：", my_string)
    return my_string
def replace_str(original_string):
    tstr= original_string.replace(' ', '').replace('\t', '').\
        replace('【', '[').replace('】', ']').replace('\n','').replace('\r','').\
        replace('：', ':').replace("（", "(").replace("）", ")").replace('\r\n','').replace('、','').replace('☐','')


    new_str1=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]',"", tstr)
    new_str = re.sub(r'[\n\r]', ' ',new_str1 )
    return new_str

def str_valid(row):
    return (row == "\n" or row == "\t" or row == " ")


def all_match(rule, target_str):
    l = []
    for i in rule:
        l.append(target_str.find(i) != -1)

    return all(l)

# just one true , result true
def any_match(rule, target_str):
    l = []
    for i in rule:
        l.append(target_str.find(i) != -1)

    return any(l)


def split_str(s: str, split_str: str):
    if s.find(split_str) != -1:
        return [replace_str(v) for v in s.split(split_str)]
    else:
        return [replace_str(s)]


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def find_closest_value(target_value, input_list):
    # 初始化最小差值为正无穷大
    min_difference = float('inf')
    # 初始化最接近的值和索引
    closest_value = None
    closest_index = None

    # 遍历列表中的每个元素
    for i, value in enumerate(input_list):
        # 计算当前元素与目标值的差值
        difference = abs(target_value - value)

        # 如果当前差值比之前记录的最小差值小，则更新最小差值和最接近的值及其索引
        if difference < min_difference:
            min_difference = difference
            closest_value = value
            closest_index = i

    # 返回最接近的值和其索引
    return closest_value, closest_index
