import difflib

# 读取两个文件的内容
with open('my.txt', 'r') as file1, open('my1.txt', 'r') as file2:
    file1_content = file1.readlines()
    file2_content = file2.readlines()

# # 使用 difflib 进行比较
# d = difflib.Differ()
# diff = d.compare(file1_content, file2_content)

# 输出差异
# print('\n'.join(diff))

# 使用 difflib 进行比较
d = difflib.Differ()
diff = list(d.compare(file2_content, file1_content))

# # 输出差异的行和行号
# for i, line in enumerate(diff, 1):
#     if line.startswith('-') or line.startswith('+'):
#         print(f"Line {i}: {line.strip()}")

# Output differences with highlighted lines
for i, line in enumerate(diff, 1):
    if line.startswith('-'):
        print(f"Line {i}: \033[91m{line.strip()}\033[0m")  # Use red color for lines only in file 1
    elif line.startswith('+'):
        print(f"Line {i}: \033[92m{line.strip()}\033[0m")  # Use green color for lines only in file 2
    # else:
    #     print(f"Line {i}: {line.strip()}")  # Normal lines