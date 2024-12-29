import sys
sys.path.insert(0, '.')
from core.utils import load_object_from_today, save_object_locally
from tools.plawrighttools import playwright_tools
from core.agentexecutor import ToolsAgentRunner
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json

tools = playwright_tools

tools_runner = ToolsAgentRunner(tools=tools)

"""
This workflow is intented to gather all the finance news from major internet sources,
using that summary it will give some stocks to buy
"""

outputs = {}

news_sources = [
    "https://www.wsj.com/finance",
    "https://www.cnbc.com/",
    "https://ca.finance.yahoo.com/",
]

sources = load_object_from_today()

if sources is None:
    # gather all the information
    for source in news_sources:
        print(f'Running agent for {source}')
        output = tools_runner.execute(prompt=f"Go to {source} and give me summary of all finance news mentioned on the page. Print out url at each step.")
        outputs[source] = output.get('output')
        print(f'Finished Running Agent for {source}')
else:
    outputs = sources

# send it to llm for analysis
chat = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content=f"You're a a financial news analyst assistant that has a knowledge base of latest financial news from various sources: {json.dumps(outputs)}"),
    HumanMessage(content="I need to understand the current trends in stocks and how they can inform my investing decisions, I'm looking for strategies to protect my investments in stocks in times of economic uncertainty. I need to know the key drivers and indicators that influence the performance of the stock market, I'm looking for ways to maximize my returns from stocks without taking on too much risk and I need to identify potential opportunities and threats in the stock market that could impact my investments, advice me using the information you have"),
]

analysis = ""

if outputs.get('analysis') is None:
    for chunk in chat.stream(messages):
        analysis = f"{analysis}{chunk.content} "
        print(chunk.content, end="", flush=True)
    outputs['analysis'] = analysis

save_object_locally(outputs)
