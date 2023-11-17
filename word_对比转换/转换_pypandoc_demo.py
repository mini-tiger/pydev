# apt-get install pandoc
import pypandoc

output = pypandoc.convert_file('/data/work/pydev/file_对比转换/lock2023_new.docx', 'rst', outputfile="somefile.rst")
assert output == ""