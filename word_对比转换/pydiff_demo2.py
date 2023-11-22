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

diff = difflib.ndiff(file1.splitlines(), file2.splitlines())
for line in diff:
    print(line)

print('---------\n')

differ = DifflibParser(file1.splitlines(), file2.splitlines())

for line in differ:
    print(line)


html_output_custom = '<html><body><h2>Custom Diff Parser</h2><pre>'

for line in differ:
    print(line)
    if line['code'] == DiffCode.LEFTONLY:
        html_output_custom += f'<span style="background-color: #ff9999;">{line["line"]}</span><br>'
    elif line['code'] == DiffCode.RIGHTONLY:
        html_output_custom += f'<span style="background-color: #99ff99;">{line["line"]}</span><br>'
    elif line['code'] == DiffCode.CHANGED:
        html_output_custom += f'<span style="background-color: #11ee11;">{line["line"]}</span><br>'
    else:
        html_output_custom += f'{line["line"]}<br>'

html_output_custom += '</pre></body></html>'

with open('diff_output_custom_parser.html', 'w') as file:
    file.write(html_output_custom)