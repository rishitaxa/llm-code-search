from fastapi import APIRouter
from pydantic import BaseModel
from .search_engine import CodeSearchEngine

router = APIRouter()
engine = CodeSearchEngine()

class IndexReq(BaseModel):
    path: str

class SearchReq(BaseModel):
    query: str

@router.post("/index")
def index_code(req: IndexReq):
    engine.index_directory(req.path)
    return {"status": "indexed"}

@router.post("/search")
def search(req: SearchReq):
    return engine.search(req.query)
