import os

os.environ["HTTP_PROXY"] = "http://172.22.50.191:1081"
os.environ["HTTPS_PROXY"] = "http://172.22.50.191:1081"
from phasellm.eval import GPTEvaluator, HumanEvaluatorCommandLine

# We'll use GPT-3.5 as the evaluator (default for GPTEvaluator).
# e = GPTEvaluator("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")

e = HumanEvaluatorCommandLine()
from phasellm.llms import CohereWrapper, ClaudeWrapper, OpenAIGPTWrapper

cohere_model = CohereWrapper("KWsWAppR88bt217wfnFvzxbPopETN6bO5xgk0clX")
# openai_model = OpenAIGPTWrapper("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")
# claude_model = ClaudeWrapper(anthropic_api_key)

# print(openai_model.complete_chat("I'm planning to visit Poland in spring."))
objective = "你知道世纪互联这家公司吗"

# Chats that have been launched by users.
# travel_chat_starts = [
#     "I'm planning to visit Poland in spring.",
#     "I'm looking for the cheapest flight to Europe next week.",
#     "I am trying to decide between Prague and Paris for a 5-day trip",
#     "I want to visit Europe but can't decide if spring, summer, or fall would be better.",
#     "I'm unsure I should visit Spain by flying via the UK or via France."
# ]

travel_chat_starts = [
    "你知道世纪互联这家公司吗，说说它的情况,用中文回答",
]


def complete_chat1() -> str:
    return "世纪互联IDC"


print("Running test. 1 = Cohere, and 2 = Claude.")
for tcs in travel_chat_starts:
    messages = [{"role": "system", "content": objective},
                {"role": "user", "content": tcs}]

    response_cohere = cohere_model.complete_chat(messages, "assistant")
    # response_claude = claude_model.complete_chat(messages, "assistant")
    # print(response_cohere)
    pref = e.choose(objective=objective, prompt=tcs, response1=response_cohere, response2=complete_chat1())
    print(f"{pref}")
