import jionlp as jio

for line in jio.read_file_by_iter('/data/work/pydev/AI/test.txt'):
    print(line)
    res = jio.clean_text(line, remove_html_tag=False, convert_full2half=False,
                         remove_exception_char=False, remove_url=False,
                         remove_redundant_char=False, remove_parentheses=False,
                         remove_email=False, remove_phone_number=False,
                         delete_prefix=False, redundant_chars=False)
