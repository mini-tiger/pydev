# xxx https://github.com/run-llama/llama_parse
# https://github.com/run-llama/llama_parse/blob/main/examples/demo_advanced.ipynb
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# llm = OpenAI(model="gpt-3.5-turbo-0125",api_base="http://120.133.63.166:8000/v1",api_key='EMPTY')
#
# Settings.llm = llm
# Settings.embed_model = HuggingFaceEmbedding(
#     model_name="/data/work/pydev/ai-reporter/webapi/db/m3e-base"
# )


from llama_parse import LlamaParse

documents = LlamaParse(result_type="markdown",verbose=True,api_key='llx-8pizWDxh0WIduzb2b6bRYbc8xvelug40sD1XarcQkW9afNHo').load_data('./uber_10q_march_2022.pdf')
print(documents)