import os

# from unstructured.partition.email import partition_email
# os.chdir("/data/work/pydev/AI/unstructured/example-docs/eml")
# elements = partition_email(filename="fake-email.eml")
#
def printele(elements):
    # print(elements)
    for i in elements:
        print(i)
    print("-" * 100)

# with open("fake-email.eml", "r") as f:
#     elements = partition_email(file=f)
#
# printele(elements)
# with open("fake-email.eml", "r") as f:
#     text = f.read()
# elements = partition_email(text=text)
# printele(elements)
# with open("fake-email.eml", "r") as f:
#     text = f.read()
# elements = partition_email(text=text, content_source="text/plain")
# printele(elements)
# with open("fake-email.eml", "r") as f:
#     text = f.read()
# elements = partition_email(text=text, include_headers=True)
# printele(elements)


from unstructured.partition.auto import partition
from unstructured.partition.email import partition_email

filename = "/data/work/pydev/AI/unstructured/example-docs/fake-email-attachment.msg"
elements = partition_email(
  filename=filename, process_attachments=True, attachment_partitioner=partition
)
printele(elements)