import csv
import codecs

# 定义输入文件名和输出文件名
input_file = 'abc.csv'
output_file = 'output.csv'

# 打开输入文件以GBK编码方式读取
with codecs.open(input_file, 'r', encoding='gbk', errors='ignore') as f:
    reader = csv.reader(f)

    # 打开输出文件以UTF-8编码方式写入
    with codecs.open(output_file, 'w', encoding='utf-8') as fout:
        writer = csv.writer(fout)

        # 逐行读取输入文件，并写入到输出文件
        for row in reader:
            # 在这里你可能需要对每一行进行一些处理，然后再写入输出文件
            # 例如，可以对每一列进行处理，或者删除某些行
            writer.writerow(row)
