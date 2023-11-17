from pydiff import *

file1 = '''
line1
lineTwo
lineThrees
line4
line6
linefile1
'''

file2 = '''
line1
xlineTw0
lineThree
line4
line66
fileline2
'''

with open("/data/work/pydev/file_diff/lock2023.docx.txt", 'r') as file1, open("/data/work/pydev/file_diff/lock2023-1.docx.txt", 'r') as file2:
    file1_content = file1.readlines()
    file2_content = file2.readlines()


html_output = '<html><head><meta charset="UTF-8"></head><body><h2>Custom Diff Parser</h2><pre>'

differ = DifflibParser(file1_content, file2_content)
# file1_lines = file1.splitlines()
# file2_lines = file2.splitlines()
line_number = 0  # Initialize line number counter
for line in differ:

    if line['code'] == DiffCode.LEFTONLY:
        html_output += f'<span style="background-color: #ff9999;">{line["line"]}</span><br>'
    elif line['code'] == DiffCode.RIGHTONLY:
        html_output += f'<span style="background-color: #99ff99;">{line["line"]}</span><br>'
    elif line['code'] == DiffCode.CHANGED:
        leftchanges = line.get('leftchanges', [])
        rightchanges = line.get('rightchanges', [])
        new_line = list(line['newline'])

        # Highlight individual different characters in red and green
        for i in range(len(new_line)):
            if i in leftchanges:
                new_line[i] = f'<span style="background-color: #ff9999;">{new_line[i]}</span>'
            if i in rightchanges:
                new_line[i] = f'<span style="background-color: #99ff99;">{new_line[i]}</span>'

        html_output += ''.join(new_line) + '<br>'
    else:
        html_output += f'{line["line"]}<br>'

    line_number += 1  # Increment the line number for each line

html_output += '</pre></body></html>'

with open('diff_output_custom_parser.html', 'w',encoding='utf-8') as file:
    file.write(html_output)