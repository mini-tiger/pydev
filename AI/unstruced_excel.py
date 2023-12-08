import os

from unstructured.partition.xlsx import partition_xlsx
os.chdir("/data/work/pydev/AI/unstructured")
elements = partition_xlsx(filename="example-docs/stanley-cups.xlsx")
print(elements[0].metadata.text_as_html)