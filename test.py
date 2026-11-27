import os
import numpy as np
from pypdf import PdfReader
from openai import OpenAI
import re

folder=r"D:\VS CODE\VS CODE 项目\data"
pdf_files=[f for f in os.listdir(folder)if f.lower().endswith(".pdf")]
first_pdf=os.path.join(folder,pdf_files[0])
reader=PdfReader(first_pdf)

chunk_size=500
chunk_overlap=50
pages_to_read = range(10, 60)

def is_toc(chunk):
    return bool(re.search(r"\.{5,}", chunk)) and bool(re.search(r"\b\d+-\d+\b", chunk))
all_chunks = []
for page_num in pages_to_read:
    page_text = reader.pages[page_num].extract_text() or ""
    if len(page_text.strip()) < 100:   # 空白页或图片页，跳过
        continue

    start = 0
    while start < len(page_text):
        end = start + chunk_size
        chunk = page_text[start:end]
        if not is_toc(chunk):
            all_chunks.append(chunk)
        start = end - chunk_overlap
            
for i, c in enumerate(all_chunks):
    if "Hydraulic Fluid" in c and "....." not in c:
        print(i, c[:200])
        break

print("总页数：", len(list(pages_to_read)))
print("总段数：", len(all_chunks))

client=OpenAI(
    api_key="ak-18919ed5ea5ee9b50f05c3e69df1f182",
    base_url="https://maas-api.cn-huabei-1.xf-yun.com/v2"
)


all_vectors = []
for i, chunk in enumerate(all_chunks):
    response = client.embeddings.create(
        model="xop3qwen8bembedding",
        input=chunk
    )
    all_vectors.append(response.data[0].embedding)
    if (i + 1) % 50 == 0:
        print(f"已完成 {i + 1} / {len(all_chunks)}")

print("测试段数：", len(all_chunks))
print("向量数量：", len(all_vectors))
print("第一个向量维度：", len(all_vectors[0]))
print("维度是否全部一致：", all(len(v) == len(all_vectors[0]) for v in all_vectors))
questions = [
    "副翼铰链为什么装在重心后方？",
    "升降舵控制什么？",
    "方向舵怎么工作？",
    "飞行控制面有哪些？",
    "液压系统用在什么地方？",
]

for question in questions:
    print("\n" + "=" * 60)
    print("问题：", question)

    q_response = client.embeddings.create(
        model="xop3qwen8bembedding",
        input=question
    )
    q_vector = q_response.data[0].embedding

    scores = []
    for vec in all_vectors:
        a = np.array(q_vector)
        b = np.array(vec)
        score = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        scores.append(score)

    top_k = 5
    top_idx = np.argsort(scores)[::-1][:top_k]
    print("top1 分数：", round(float(scores[top_idx[0]]), 4))
    print("top1 开头：", all_chunks[top_idx[0]][:80].replace("\n", " "))

    context = "\n\n".join([all_chunks[i] for i in top_idx])

    prompt = f"""你是一个航空维修助手。请根据下面资料回答问题。如果资料中有相关内容，请直接回答；如果资料确实不包含答案，再说明"资料未提及"。

资料:
{context}

问题:{question}
"""

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="spark-x2.6-4b",
        messages=messages
    )

    answer = response.choices[0].message.content
    if "</think" in answer:
        answer = answer.split("</think")[-1].strip()
    print("模型回答：", answer)

    if "液压系统" in question:
        print("\n----- Q5 top5 -----")
        for rank, idx in enumerate(top_idx, 1):
            print(f"\n第{rank}名 分数 {round(float(scores[idx]), 4)}:")
            print(all_chunks[idx][:200])
        print("----- 结束 -----\n")