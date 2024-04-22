
class UtilTools():

    def digit_to_chinese(self,num):
        digit_list = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        unit_list = ['', '十', '百', '千', '万']
        
        if num < 0:
            return "请输入非负整数"
        if num < 10:
            return digit_list[num]
        
        result = ''
        num_str = str(num)
        length = len(num_str)
        for i, digit in enumerate(num_str):
            digit = int(digit)
            if digit != 0:
                result += digit_list[digit] + unit_list[length - i - 1]
            else:
                if i < length - 1 and int(num_str[i + 1]) != 0:
                    result += digit_list[digit]
        return result