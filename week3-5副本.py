import os
import numpy as np
from pypdf import PdfReader
from openai import OpenAI
import re

client=OpenAI(
    api_key="ak-18919ed5ea5ee9b50f05c3e69df1f182",
    base_url="https://maas-api.cn-huabei-1.xf-yun.com/v2"
)

folder=r"D:\VS CODE\VS CODE 项目\data"
pdf_files=[f for f in os.listdir(folder)if f.lower().endswith(".pdf")]
first_pdf=os.path.join(folder,pdf_files[0])
reader=PdfReader(first_pdf)
page_text=reader.pages[50].extract_text()or""

chunk_size=500
chunk_overlap=50
chunks=[]
start=0
while start<len(page_text):
    end=start+chunk_size
    chunk=page_text[start:end]
    chunks.append(chunk)
    start=end-chunk_overlap

vectors=[]
for chunk in chunks:
    response=client.embeddings.create(
        model="xop3qwen8bembedding",
        input=chunk
    )
    vectors.append(response.data[0].embedding)

questions=[
    "副翼铰链为什么装在重心后方？",
    "副翼铰链为什么装在重心前面？",
    "用什么装置防止副翼颤振？",
    "液压油多久更换一次？",
    "副翼和升降舵分别控制什么？",
    "飞行控制面有哪些",
    ]

clean_chunks=[re.sub(r"\s+"," ",c).strip()for c in chunks]

for question in questions:
    print("\n"+"="*60)
    print("问题:",question)

    q_response=client.embeddings.create(
    model="xop3qwen8bembedding",
    input=question
    )
    q_vector=q_response.data[0].embedding

    scores=[]
    for vec in vectors:
        a=np.array(q_vector)
        b=np.array(vec)
        score=np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
        scores.append(score)

    top_k=5
    top_idx=np.argsort(scores)[::-1][:top_k]
    print("top1分数:",round(float(scores[top_idx[0]]),4))
    print("top1开头:",chunks[top_idx[0]][:80].replace("\n"," "))

    if "副翼和升降舵" in question or "飞行控制面有哪些" in question:
        print("\n----- top5 完整内容 -----")
        for rank, idx in enumerate(top_idx, 1):
            print(f"\n第{rank}名 分数 {round(float(scores[idx]), 4)}:")
            print(clean_chunks[idx][:150])
        print("----- top5 结束 -----\n")

    context="\n\n".join([clean_chunks[i]for i in top_idx])

    prompt=f"""你是一个航空维修助手。请只根据下面资料回答问题，如果资料中有相关内容，请直接回答；如果资料确实不包含答案，再说明"资料未提及"。

    资料:
    {context}

    问题:{question}
    """

    if"重心后方"in question:
        print("\n=====Q1完整prompt=====")
        print(prompt)
        print("=====prompt结束=====\n")
    messages=[{"role":"user","content":prompt}]
    response=client.chat.completions.create(
    model="spark-x2.6-4b",
    messages=messages
    )

    answer=response.choices[0].message.content
    if"</think"in answer:
        answer=answer.split("</think")[-1].strip()
    print("模型回答:",answer)