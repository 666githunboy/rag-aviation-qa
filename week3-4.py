from openai import OpenAI
import os
from pypdf import PdfReader

client=OpenAI(
    api_key="ak-18919ed5ea5ee9b50f05c3e69df1f182",
    base_url="https://maas-api.cn-huabei-1.xf-yun.com/v2"
)

folder=r"D:\VS CODE\VS CODE 项目\data"
pdf_files=[f for f in os.listdir(folder)if f.lower().endswith(".pdf")]
first_pdf=os.path.join(folder,pdf_files[0])
reader=PdfReader(first_pdf)
page_text=reader.pages[50].extract_text()or" "

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

print("chunk数量:",len(chunks))
print("向量数量:",len(vectors))
print("每个向量的维度:",len(vectors[0]))