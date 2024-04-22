# https://github.com/run-llama/llama_index/blob/main/docs/examples/node_postprocessor/FlagEmbeddingReranker.ipynb

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# load documents
documents = SimpleDirectoryReader("/data/work/pydev/ai-reporter/webapi/pdf").load_data()

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

# Settings.llm = OpenAI(model="gpt-3.5-turbo")
Settings.llm = None
Settings.embed_model = HuggingFaceEmbedding(
    model_name="/data/work/pydev/ai-reporter/webapi/db/m3e-base"
)

index = VectorStoreIndex.from_documents(documents=documents)




from llama_index.postprocessor.flag_embedding_reranker import (
    FlagEmbeddingReranker,
)

rerank = FlagEmbeddingReranker(model="/data/work/pydev/ai-reporter/webapi/db/bge-reranker-base", top_n=5)
query_engine = index.as_query_engine(
    similarity_top_k=10, node_postprocessors=[rerank]
)
from time import time
now = time()
response = query_engine.query(
    "研究背景及意义",
)
print(response)
print(f"Elapsed: {round(time() - now, 2)}s")