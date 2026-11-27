import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

from rag_qa import load_pdf_chunks, embed_chunks, search, generate_answer

client = OpenAI(
    api_key=os.environ["XFYUN_API_KEY"],
    base_url=os.environ["XFYUN_BASE_URL"]
)

app = FastAPI(title="RAG Aviation QA API")

folder = r"D:\VS CODE\VS CODE 项目\data"
pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
first_pdf = os.path.join(folder, pdf_files[0])

chunks = load_pdf_chunks(first_pdf, range(10, 60))
vectors = embed_chunks(chunks, client)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


class AskResponse(BaseModel):
    question: str
    answer: str
    top_pages: list[int]
    top_score: float


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    top_idx, scores = search(req.question, chunks, vectors, client, top_k=req.top_k)
    answer = generate_answer(req.question, chunks, top_idx, client)
    return AskResponse(
        question=req.question,
        answer=answer,
        top_pages=[chunks[i][0] for i in top_idx],
        top_score=round(float(scores[top_idx[0]]), 4)
    )