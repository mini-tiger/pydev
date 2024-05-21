from pydiff_gui.difflibparser.difflibparser import DiffCode, DifflibParser
import copy



with open("my.txt", 'r') as file1, open("my1.txt", 'r') as file2:
    file1_content = file1.readlines()
    file2_content = file2.readlines()


differ = DifflibParser(file1_content, file2_content)

for line in differ:
    print(line)
    leftchanges = line.get('leftchanges', [])
    rightchanges = line.get('rightchanges', [])

    new_line_list = list(line['newline'])
    line_list =list(line['line'])
    output_line=copy.deepcopy(line_list)
    output_newline=copy.deepcopy(new_line_list)
    # Highlight individual different characters in red and green
    # for i in range(len(line_list)):
    for ii in leftchanges:
        output_line[ii] = f'<span style="background-color: #ff9999;">{line_list[ii]}</span>'

    for i in rightchanges:
        output_newline[i] = f'<span style="background-color: #99ff99;">{new_line_list[i]}</span>'
    print(output_line)
    print(output_newline)
