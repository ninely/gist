"""This is an example of how to use agent to return final streaming result."""
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.agents import load_tools
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler
from langchain.llms import OpenAI

# Two ways to load env variables
# 1.load env variables from .env file
load_dotenv()

# 2.manually set env variables
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = ""

app = FastAPI()


def do_agent():
    question = "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
    callback = FinalStreamingStdOutCallbackHandler()
    stream_llm = OpenAI(
        temperature=0,
        streaming=True,
        verbose=True,
        callbacks=[callback],
    )
    tools = load_tools(["ddg-search", "llm-math"], llm=stream_llm)
    agent = initialize_agent(tools, stream_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    agent.run(question)


if __name__ == "__main__":
    do_agent()
