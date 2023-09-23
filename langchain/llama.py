import asyncio
import os

from langchain.callbacks import AsyncIteratorCallbackHandler, StdOutCallbackHandler
from my_llamacpp import LlamaCpp
# from langchain.llms import LlamaCpp

from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager, AsyncCallbackManager
from dotenv import load_dotenv

load_dotenv()
template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"


async def run():
    handler = StdOutCallbackHandler()
    callback_manager = CallbackManager([handler])

    llm = LlamaCpp(
        model_path=os.environ["MODEL_PATH"],
        callback_manager=callback_manager,
        verbose=True,
        streaming=False,
    )

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return await llm_chain.arun(question)


async def run_stream():
    handler = AsyncIteratorCallbackHandler()
    callback_manager = AsyncCallbackManager([handler])

    stream_llm = LlamaCpp(
        model_path=os.environ["MODEL_PATH"],
        callback_manager=callback_manager,
        verbose=True,
        streaming=True,
    )
    llm_chain = LLMChain(prompt=prompt, llm=stream_llm)

    async def read():
        async for token in handler.aiter():
            print(token, end="")

    return await asyncio.gather(llm_chain.arun(question), read())


result = asyncio.run(run_stream())
print("result: ", result)
