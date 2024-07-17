
from operator import itemgetter
import os

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

# Initialize chat model
import os

from langchain_core.messages import AIMessage

os.environ["OPENAI_API_KEY"] = 'EMPTY'
llm = ChatOpenAI(temperature=0,openai_api_base="http://120.133.83.145:8000/v1")
print(dir(llm))
# Define a prompt template
template = """You are a helpful AI assistant. You give specialized advice on travel.
"""

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# Create conversation history store
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | chat_prompt
    | llm
)


def stream_response(message, history):
    print(f"Input: {message}. History: {history}\n")

    if history:
        human, ai = history[-1]
        from langchain_core.messages import HumanMessage
        memory.chat_memory.add_user_message(human)
        memory.chat_memory.add_ai_message(ai)

    print(f"Memory in chain: \n{memory.chat_memory} \n")

    if message is not None:
        partial_message = ""
        # ChatInterface struggles with rendering stream
        for response in chain.stream({"input": message}):
            partial_message += response.content
            # print(partial_message)
            yield partial_message


# UI
import gradio as gr


with gr.Blocks(title="Langchain + Llama-index with Baichuan-13B", analytics_enabled=False) as demo:
    with gr.Row():
        gr.Label("Langchain + Llama-index with Baichuan-13B", show_label=False)
    with gr.Row():
        # system_prompt = gr.Textbox("You are helpful AI.", label="System Prompt")
        slider = gr.Slider(10, 100, render=False)

        gr.ChatInterface(
            stream_response
        )

demo.queue().launch(server_name="0.0.0.0", share=False)


# with gr.Blocks(title="Langchain + Llama-index with Baichuan-13B", analytics_enabled=False) as demo:
#     with gr.Row():
#         gr.Label("Langchain + Llama-index with Baichuan-13B", show_label=False)
#     with gr.Row():
#         with gr.Column(scale=5):
#             gr.HTML(
#                 '<a href="https://gitlab.dev.21vianet.com/sbg2-neolinkgpt/neolink-dataset/-/issues/new">页面使用中如有任何问题或需求，请点击此链接开Issue。</a>')
#             gr.HTML(f'''<p>当前提供的检索信息包括：
#                     <a href="{BaseConfig.API_URL}/上海静安数据中心信息大纲文本.txt">上海静安数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/中国联通华东云数据中心.txt">中国联通华东云数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/外高桥数据中心信息汇总_20230905.txt">外高桥数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/广东佛山永丰数据中心.txt">广东佛山永丰数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/广州亚太信息引擎数据中心.txt">广州亚太信息引擎数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/广网互联大学城数据中心.txt">广网互联大学城数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/杭州滨安路数据中心.txt">杭州滨安路数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/杭州滨江数据中心.txt">杭州滨江数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/杭州石桥数据中心.txt">杭州石桥数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/荷丹数据中心.txt">荷丹数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/（ORC扫描版）世纪互联云传输白皮书（beta版）_2017年8月.txt">世纪互联云传输白皮书（beta版）_2017年8月</a>、
#                     <a href="{BaseConfig.API_URL}/CCIB+静态带宽产品白皮书170428.txt">CCIB+静态带宽产品白皮书170428</a>、
#                     <a href="{BaseConfig.API_URL}/世纪互联CDN产品白皮书v1.txt">世纪互联CDN产品白皮书v1</a>、
#                     <a href="{BaseConfig.API_URL}/世纪互联DC产品规划白皮书-上海外高桥数据中心.txt">世纪互联DC产品规划白皮书-上海外高桥数据中心</a>、
#                     <a href="{BaseConfig.API_URL}/世纪互联DC产品规划白皮书-四川川北云计算大数据中心项目-201903V3.0.txt">世纪互联DC产品规划白皮书-四川川北云计算大数据中心项目-201903V3.0</a>、
#                     <a href="{BaseConfig.API_URL}/互联科技AGI 产品与解决方案销售指导书.md">互联科技AGI 产品与解决方案销售指导书</a>、
#                     <a href="{BaseConfig.API_URL}/全域托管云白皮书.txt">全域托管云白皮书</a>、
#                     <a href="{BaseConfig.API_URL}/超互联新算力网络白皮书-世纪互联发布-2022.txt">超互联新算力网络白皮书-世纪互联发布-2022</a>、
#                     <a href="{BaseConfig.API_URL}/超级连接产品白皮书.v0.6.20170221.txt">超级连接产品白皮书.v0.6.20170221</a>。
#             </p>''')
#     with gr.Row():
#         with gr.Column(scale=5):
#             drpLLM = gr.Dropdown(choices=llm_urls, label="请选择LLM:", value=llm_urls[0])
#             drpLLM.change(fn=select_llm, inputs=[drpLLM])
#     with gr.Row():
#         with gr.Column(scale=2):
#             history_content = gr.Textbox(label="已评估的内容", lines=23, interactive=False)
#         with gr.Column(scale=3):
#             drpUser = gr.Dropdown(choices=["patrick", "matthew", "rain", "leo", "gary"], label="请选择用户名:",
#                                   value="matthew")
#             drpUser.change(fn=handle, inputs=[drpUser])
#             handle("matthew")
#             output_content = gr.Textbox(label="输出的结果", lines=3)
#             with gr.Row():
#                 with gr.Column(scale=4):
#                     rdoScore = gr.Radio(["错误", "有偏差", "无意见", "较好", "很好"], label="请评分:")
#                     rdoScore.change(fn=score, inputs=[rdoScore, drpUser], outputs=[history_content])
#                 with gr.Column(scale=1):
#                     numScore = gr.Number(label="系统评分", value=0.0, interactive=False)
#             input_content = gr.Textbox(label="输入的问题", lines=2, value="")
#             btn_query = gr.Button("检索查询")
#             btn_query.click(evaluate, inputs=[input_content, rdoScore, drpUser, drpLLM],
#                             outputs=[output_content, numScore])
#             gr.on(triggers=[btn_query.click], fn=resetRdo, outputs=[rdoScore], postprocess=True)
# demo.launch(server_name="0.0.0.0", share=False)
