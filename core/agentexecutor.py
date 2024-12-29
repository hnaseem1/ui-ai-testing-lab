from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub

class NoToolKitDefinedException:
    pass

class ToolsAgentRunner:
    def __init__(self, tools=None, prompt=None, model="gpt-4o-mini"):

        if tools is None:
            raise NoToolKitDefinedException("tools are required")
        self.tools = tools
        if prompt is None:
            prompt = hub.pull("hwchase17/openai-tools-agent")
        llm = ChatOpenAI(model=model, temperature=0)
        self.agent = create_openai_tools_agent(llm, tools, prompt)

    def execute(self, prompt):
        agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)
        command = {
            "input": prompt
        }
        return agent_executor.invoke(command)