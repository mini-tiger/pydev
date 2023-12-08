'''欢迎来到LangChain实战课
https://time.geekbang.org/column/intro/100617601
作者 黄佳'''
# 设置OpenAI API密钥
import os
from langchain.chat_models import ChatOpenAI
# 初始化大模型
# llm = OpenAI(temperature=0)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default="EMPTY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", default="http://120.133.83.145:8000/v1")
OPENAI_PROXY = os.environ.get("OPENAI_PROXY", default="")

os.environ.setdefault("OPENAI_API_KEY", OPENAI_API_KEY)
os.environ.setdefault("OPENAI_API_BASE", OPENAI_API_BASE)

llm = ChatOpenAI(
    openai_api_base=OPENAI_API_BASE,
    openai_api_key=OPENAI_API_KEY,
    openai_proxy=OPENAI_PROXY,
    temperature=0,
    # callbacks=[self.cb],
)

# 导入所需库
from langchain import PromptTemplate, OpenAI, LLMChain

# 设置提示模板
prompt = PromptTemplate(
    input_variables=["flower", "season"],
    template="{flower}在{season}的花语是?"
)



# 初始化链
llm_chain = LLMChain(llm=llm, prompt=prompt)

# 调用链
response = llm_chain({
    'flower': "玫瑰",
    'season': "夏季"
})
print(response)

# run方法
llm_chain.run({
    'flower': "玫瑰",
    'season': "夏季"
})

# predict方法 predict 与 run 方法类似，只不过输入键被指定为关键字参数而不是 Python 字典。
result = llm_chain.predict(flower="玫瑰", season="夏季")
print(result)

# apply方法允许您针对输入列表运行链
input_list = [
    {"flower": "玫瑰", 'season': "夏季"},
    {"flower": "百合", 'season': "春季"},
    {"flower": "郁金香", 'season': "秋季"}
]
result = llm_chain.apply(input_list)
print(result)

# generate方法
result = llm_chain.generate(input_list)
print(result)