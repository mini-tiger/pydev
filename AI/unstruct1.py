from unstructured.partition.auto import partition
import os
import nltk
nltk.set_proxy('http://127.0.0.1:1081')
# nltk.download('punkt')
basedir = "/data/work/pydev/AI/unstructured"
#
# elements = partition(filename=os.path.join(basedir, "example-docs/example-10k.html"))
# print(elements)

from unstructured.partition.csv import partition_csv

elements = partition_csv(filename="/mnt/1.csv")
# print(elements[0].metadata.text_as_html)
# print(elements[0].metadata.text_as_html)

from unstructured.staging.base import dict_to_elements

isd = [
  {"text": "My Title", "type": "Title"},
  {"text": "My Narrative", "type": "NarrativeText"}
]

# elements will look like:
# [ Title(text="My Title"), NarrativeText(text="My Narrative")]
elements = dict_to_elements(isd)
print(elements[0].to_dict())


import json

from unstructured.documents.elements import Title, NarrativeText
from unstructured.staging.label_studio import stage_for_label_studio

elements = [Title(text="Title"), NarrativeText(text="Narrative")]
label_studio_data = stage_for_label_studio(elements, text_field="my_text", id_field="my_id")

# The resulting JSON file is ready to be uploaded to LabelStudio
with open("label_studio.json", "w") as f:
    json.dump(label_studio_data, f, indent=4)


import json

from unstructured.documents.elements import NarrativeText
from unstructured.staging.label_studio import (
    stage_for_label_studio,
    LabelStudioAnnotation,
    LabelStudioPrediction,
    LabelStudioResult,
)

risk_section = [NarrativeText(text="Risk section 1"), NarrativeText(text="Risk section 2")]
annotations = []
for element in risk_section:
    annotations.append([LabelStudioAnnotation(
          result=[
              LabelStudioResult(
                  type="choices",
                  value={"choices": ["Positive"]},
                  from_name="sentiment",
                  to_name="text",
              )
          ]
      )]
    )


predictions = []
for element in risk_section:
    predictions.append([LabelStudioPrediction(
          result=[
              LabelStudioResult(
                  type="choices",
                  value={"choices": ["Positive"]},
                  from_name="sentiment",
                  to_name="text",
              )
          ],
          score=0.68
      )]
    )

label_studio_data = stage_for_label_studio(
    elements=risk_section,
    annotations=annotations,
    predictions=predictions,
    text_field="text",
    id_field="id"
)

# The resulting JSON file is ready to be uploaded to LabelStudio
with open("label-studio.json", "w") as f:
    json.dump(label_studio_data, f, indent=4)


from unstructured.file_utils.exploration import get_directory_file_info

file_info = get_directory_file_info(os.path.join(basedir,"example-docs"))
print(file_info.filetype.value_counts())