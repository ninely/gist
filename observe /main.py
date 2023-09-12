import os

from dotenv import load_dotenv
from langchain import OpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.callbacks import FinalStreamingStdOutCallbackHandler
from langfuse.callback import CallbackHandler

load_dotenv()

LANGFUSE_PUBLIC_KEY = os.environ["LANGFUSE_PUBLIC_KEY"]
LANGFUSE_SECRET_KEY = os.environ["LANGFUSE_SECRET_KEY"]
handler = CallbackHandler(LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)

# Langchain implementation
if __name__ == "__main__":
    question = "Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?"
    callback = FinalStreamingStdOutCallbackHandler()
    stream_llm = OpenAI(
        temperature=0,
        streaming=True,
        verbose=True,
        callbacks=[callback],
    )
    tools = load_tools(["llm-math"], llm=stream_llm)
    agent = initialize_agent(tools, stream_llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent.run(question, callbacks=[handler])
