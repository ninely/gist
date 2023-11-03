from fastapi import FastAPI
from langserve import add_routes

from extraction_openai_functions import chain as extraction_openai_functions_chain

app = FastAPI()

add_routes(app, extraction_openai_functions_chain, path="/extraction-openai-functions")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
