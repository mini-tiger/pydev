def replace_str(original_string):
    string_without_spaces = original_string.replace(' ', '')
    string_without_tab=string_without_spaces.replace('\t','')
    return string_without_tab.replace('\n', '')

def str_valid(row):
    return (row == "\n" or row == "\t" or row == " ")


def find_context(elem,target_str,up=1):
    for i, value in enumerate(elem):
        if elem[i].text == target_str:
            return elem[i + up].text