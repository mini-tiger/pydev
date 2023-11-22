def replace_str(original_string):
    string_without_spaces = original_string.replace(' ', '')
    string_without_tab = string_without_spaces.replace('\t', '')
    return string_without_tab.replace('\n', '')


def str_valid(row):
    return (row == "\n" or row == "\t" or row == " ")


def find_context(elem, target_str, up=1):
    for i, value in enumerate(elem):
        if elem[i].text == target_str:
            return elem[i + up].text




def split_str(s: str,split_str:str):
    if s.find(split_str) != -1:
        return [replace_str(v) for v in s.split(split_str)]
    else:
        return [replace_str(s)]
