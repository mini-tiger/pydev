from pydiff import *

# file1 = '''
# line1
# lineTwo
# lineThrees
# line4
# line6
# linefile1
# '''
#
# file2 = '''
# line1
# xlineTw0
# lineThree
# line4
# line66
# fileline2
# '''

with open("/data/work/pydev/file_对比转换/lock2023_new.docx.txt", 'r') as file1, open("/data/work/pydev/file_对比转换/convert_test/带宽罚则 非锁定版(非标准合同)_IDC主协议_北京世纪互联宽带数据中心托管服务协议(2023年版)-（非预留机柜）_modify.txt", 'r') as file2:
    file1_content = file1.readlines()
    file2_content = file2.readlines()

html_output = '''
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h2>Custom Diff Parser</h2>
    <table border="1">
        <tr>
            <th>Number</th>
            <th>Comparison Result</th>
        </tr>
'''
print(len(file1_content))
print(len(file2_content))
differ = DifflibParser(file1_content, file2_content)
line_number = 0

for line in differ:

    if line['code'] > 0:
        line_number += 1
        html_output += f'<tr><td>{line_number}</td>'
        if line['code'] == DiffCode.LEFTONLY:
            html_output += f'<td><span style="background-color: #ff9999;">{line["line"]}</span></td></tr>'
        elif line['code'] == DiffCode.RIGHTONLY:
            html_output += f'<td><span style="background-color: #99ff99;">{line["line"]}</span></td></tr>'
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

            html_output += f'<td>{"".join(new_line)}</td></tr>'
    # else:
    #     html_output += f'<td>{line["line"]}</td></tr>'

html_output += '''
    </table>
</body>
</html>
'''

with open('diff_output_custom_parser.html', 'w', encoding='utf-8') as file:
    file.write(html_output)