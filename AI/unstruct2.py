from unstructured.partition.pdf import partition_pdf

# Returns a List[Element] present in the pages of the parsed pdf document
# elements = partition_pdf('/mnt/m6.pdf')

# Applies the English and Swedish language pack for ocr. OCR is only applied
# if the text is not available in the PDF.

elements = partition_pdf('/mnt/m6.pdf', ocr_languages="chi", max_partition=None)

# for el in elements:
#     print(el.to_dict())

f = open('test.txt', 'w')
for el in elements:
    if el.metadata.page_number == 3:
        print(el.to_dict())
        f.write(el.to_dict().get("text"))
        f.write("\n")

f.close()
