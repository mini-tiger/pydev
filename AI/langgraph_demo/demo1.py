import json
import operator
from typing import TypedDict, Annotated, Sequence

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation


class WeatherInput(BaseModel):
    location: str = Field(description="get temperature for a specific location")


@tool("amap_weather", args_schema=WeatherInput, return_direct=False)
def amap_weather(location: str) -> str:
    """获取指定城市的天气信息"""
    return f"{location}的天气晴朗，温度为10摄氏度"


tools = [amap_weather]
tool_executor = ToolExecutor(tools)
llm = ChatOpenAI(openai_api_key="test", openai_api_base="http://120.133.63.166:8003/v1", temperature=0)


model = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    # If there is no function call, then we finish
    if "tool_calls" not in last_message.additional_kwargs:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


# Define the function that calls the model
def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    # print(f"the model call response is {response}")
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function to execute tools
def call_tool(state):
    messages = state['messages']
    # Based on the continue condition
    # we know the last message involves a function call
    last_message = messages[-1]
    # We construct an ToolInvocation from the function_call
    action = ToolInvocation(
        tool=last_message.additional_kwargs["tool_calls"][0]["function"]["name"],
        tool_input=json.loads(last_message.additional_kwargs["tool_calls"][0]["function"]["arguments"]),
    )
    # We call the tool_executor and get back a response
    response = tool_executor.invoke(action)
    # We use the response to create a FunctionMessage
    tool_message = ToolMessage(content=str(response),
                               tool_call_id=last_message.additional_kwargs["tool_calls"][0]["id"])
    # We return a list, because this will get added to the existing list
    # print(f"the tool call response is {response}")
    return {"messages": [tool_message]}


# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("action", call_tool)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
    # Finally we pass in a mapping.
    # The keys are strings, and the values are other nodes.
    # END is a special node marking that the graph should finish.
    # What will happen is we will call `should_continue`, and then the output of that
    # will be matched against the keys in this mapping.
    # Based on which one it matches, that node will then be called.
    {
        # If `tools`, then we call the tool node.
        "continue": "action",
        # Otherwise we finish.
        "end": END
    }
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge('action', 'agent')

# Finally, we compile it!
# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
app = workflow.compile()

inputs = {"messages": [HumanMessage(content="今天北京的温度是多少？")]}
output = app.invoke(inputs)
print(output)

