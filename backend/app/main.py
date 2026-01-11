from fastapi import FastAPI
from .api import router

app = FastAPI(title="LLM Code Search")
app.include_router(router)
