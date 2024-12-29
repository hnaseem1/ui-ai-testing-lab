from tools.plawrighttools import playwright_tools
from core.agentexecutor import ToolsAgentRunner

tools = playwright_tools

tools_runner = ToolsAgentRunner(tools=tools)
output = tools_runner.execute(prompt="Go to https://www.cnbc.com/ and give me summary of all finance news mentioned on the page. Print out url at each step.")

print(output.get('output'))