import os
from langchain.memory import ConversationBufferMemory
from langchain.schema import AgentAction, AgentFinish
from typing import List, Union
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import BaseChatPromptTemplate
from langchain.prompts.chat import HumanMessage
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.utilities import BashProcess
import re
from langchain import GoogleSearchAPIWrapper, HuggingFaceHub, SerpAPIWrapper
from langchain.llms import GPT4All
from langchain.callbacks.base import CallbackManager


# Aristotle: Plato, I understand your belief in the Forms, but I believe that the true essence of things lies in their physical existence. Plato: But Aristotle, the physical world is constantly changing and imperfect. The Forms represent the true reality. Aristotle: I agree that the physical world is imperfect, but it is still real and tangible. The Forms are just abstract concepts. Plato: But Aristotle, the Forms are eternal and unchanging. They represent the ultimate truth. Aristotle: I believe that truth can be found through observation and experience, not just through abstract concepts. Plato: But Aristotle, the physical world is just a shadow of the true reality. The Forms are the only way to reach true knowledge. Aristotle: I disagree, Plato. The physical world is just as important as the world of Forms. We must study both to gain a complete understanding of reality. And so on...

# dotenv
from dotenv import load_dotenv
load_dotenv('process.env')


# Set up tools
search = GoogleSearchAPIWrapper()
bash = BashProcess()
os.environ["LANGCHAIN_HANDLER"] = "langchain"
tools = [
    Tool(
        name="Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term."
    ),
    Tool(
        name="Terminal",
        func=bash.run,
        description="useful for executing with shell commands.",
        # return_direct=True
    ),
    Tool(
        name="Error",
        func=search.run,
        description="This tool notifies you when you type a wrong format."
    ),
]

# Set up the base template
template = """You are a cooperative and friendly assistant. 
Given a history of the current conversation and a question, create a final answer. 
If it is not a question, answer by making conversation. 
To find the best answer you have to refer first to 
the History of the current conversation, and, 
if it is not enough, use any of the avaliable tools. 
##
You only have access to the following tools:
{tools}
##
Use the following format:

Question: the input question you must answer. If it is not a question, give a human response
Thought: you should always think about what to do
*Action: the action to take, it has to be one of [{tool_names}]
*Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

#
The lines starting with the * symbol are optional. If you don't use this format, you will get a "501 Wrong format" error.
##
Begin!

History of the current conversation:
{history}
Question: {input}
{agent_scratchpad}"""

# Set up a prompt template


class CustomPromptTemplate(BaseChatPromptTemplate):
    template: str
    tools: List[Tool]

    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]


prompt = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps", "history"]
)


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split(
                    "Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            return AgentAction(tool="error", tool_input="Wrong format", log=llm_output)
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)


output_parser = CustomOutputParser()

# LLM Options
llm = ChatOpenAI(temperature=0)
# llm = HuggingFaceHub(repo_id="anon8231489123/gpt4-x-alpaca-13b-native-4bit-128g",model_kwargs={"temperature": 0, "max_length": 64})
# local llm
# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# local_path = 'D:\Documentos\AI\models\gpt-x-alpaca-13b-native-4bit-128g\ggml-model-q4_1.bin'
# llm = GPT4All(model=local_path,
# callback_manager=callback_manager, verbose=True)

# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(
    llm=llm, prompt=prompt, memory=ConversationBufferMemory(input_key="input"))
tool_names = [tool.name for tool in tools]

agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    stop=["\nObservation:"],
    allowed_tools=tool_names
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True)


while (True):
    prompt = input("User: ")
    if (prompt == "exit"):
        break
    print(agent_executor.run(history=llm_chain.memory.buffer, input=prompt))
