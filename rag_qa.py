import os
import re
import numpy as np
from pypdf import PdfReader
from openai import OpenAI

folder = r"D:\VS CODE\VS CODE 项目\data"
pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
first_pdf = os.path.join(folder, pdf_files[0])


def is_toc(chunk):
    return bool(re.search(r"\.{5,}", chunk)) and bool(re.search(r"\b\d+-\d+\b", chunk))


def load_pdf_chunks(pdf_path, pages, chunk_size=500, chunk_overlap=50):
    reader = PdfReader(pdf_path)
    chunks = []
    for page_num in pages:
        page_text = reader.pages[page_num].extract_text() or ""
        if len(page_text.strip()) < 100:
            continue
        start = 0
        while start < len(page_text):
            end = start + chunk_size
            chunk = page_text[start:end]
            if not is_toc(chunk):
                cleaned = chunk.strip()
                if len(cleaned) >= 20:
                    chunks.append((page_num + 1, cleaned))
            start = end - chunk_overlap
    return chunks


def embed_chunks(chunks, client, model="xop3qwen8bembedding"):
    vectors = []
    for i, item in enumerate(chunks):
        chunk_text = item[1]
        response = client.embeddings.create(
            model=model,
            input=chunk_text
        )
        vectors.append(response.data[0].embedding)
        if (i + 1) % 50 == 0:
            print(f"已完成 {i + 1} / {len(chunks)}")
    return vectors


def search(question, chunks, vectors, client, model="xop3qwen8bembedding", top_k=5):
    q_response = client.embeddings.create(
        model=model,
        input=question
    )
    q_vector = q_response.data[0].embedding

    scores = []
    for vec in vectors:
        a = np.array(q_vector)
        b = np.array(vec)
        score = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        scores.append(score)

    top_idx = np.argsort(scores)[::-1][:top_k]
    return top_idx, scores


def generate_answer(question, chunks, top_idx, client, model="spark-x2.6-4b"):
    context = "\n\n".join([
        f"[第{chunks[i][0]}页] {chunks[i][1]}"
        for i in top_idx
    ])

    prompt = f"""你是一个航空维修助手。请根据下面资料回答问题。如果资料中有相关内容，请直接回答；如果资料确实不包含答案，再说明"资料未提及"。

资料:
{context}

问题:{question}
"""

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    answer = response.choices[0].message.content
    if "</think" in answer:
        answer = answer.split("</think")[-1].strip()
    return answer


if __name__ == "__main__":
    chunks = load_pdf_chunks(first_pdf, range(10, 60))
    print("知识库段数：", len(chunks))

    client = OpenAI(
        api_key=os.environ["XFYUN_API_KEY"],
        base_url=os.environ["XFYUN_BASE_URL"]
    )

    vectors = embed_chunks(chunks, client)
    print("向量数：", len(vectors))

    question = "副翼铰链为什么装在重心后方？"
    top_idx, scores = search(question, chunks, vectors, client)
    answer = generate_answer(question, chunks, top_idx, client)

    print("问题：", question)
    print("top1 页码：", chunks[top_idx[0]][0])
    print("模型回答：", answer)