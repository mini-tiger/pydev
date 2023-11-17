from pydiff import DifflibParser


with open("/data/work/pydev/file_diff/my.txt", 'r') as file1, open("/data/work/pydev/file_diff/my1.txt", 'r') as file2:
    file1_content = file1.readlines()
    file2_content = file2.readlines()


differ = DifflibParser(file1_content, file2_content)

for line in differ:
    print(line)
