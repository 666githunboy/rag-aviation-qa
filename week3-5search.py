import os
import numpy as np
from pypdf import PdfReader
from openai import OpenAI

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

question="副翼铰链为什么装在重心前面？"

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

print("全部分数：",[round(float(s),4)for s in scores])

top3=np.argsort(scores)[::-1][:3]
for i in top3:
    print(f"\n分数:{scores[i]:.4f}")
    print(chunks[i][:200])
    print("---")

context="\n\n".join([chunks[i]for i in top3])

prompt=f"""你是一个航空维修助手。请只根据下面资料回答问题，资料中没有相关的信息就说"资料没找到"。

资料:
{context}

问题:{question}
"""

response=client.chat.completions.create(
    model="spark-x2.6-4b",
    messages=[
        {"role":"user","content":prompt}
    ]
)

print("\n模型回答:")
print(response.choices[0].message.content)

print("我发出去的 messages:")
print([{"role": "user", "content": prompt}])

print("\n模型返回的 message:")
print(response.choices[0].message)

print("choices 长度：", len(response.choices))
print("第一条 message 的角色：",response.choices[0].message.role)
print("最终 content:",response.choices[0].message.content)