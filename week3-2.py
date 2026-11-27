import os
from pypdf import PdfReader

folder=r"D:\VS CODE\VS CODE 项目\data"
pdf_files=[f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
first_pdf=os.path.join(folder,pdf_files[0])
reader=PdfReader(first_pdf)

page_text=reader.pages[50].extract_text()or " "

chunk_size=500
chunk_overlap=50

chunks=[]
start=0
while start<len(page_text):
    end=start+chunk_size
    chunk=page_text[start:end]
    chunks.append(chunk)
    start=end-chunk_overlap

print("这一页总字符数:",len(page_text))
print("切出段数:",len(chunks))
print("\n第一段:")
print(chunks[0])
print("\n第二段:")
print(chunks[1])
print("\n第一段最后50个字符:")
print(repr(chunks[0][-50:]))
print("\n第二段开头50字符:")
print(repr(chunks[1][:50]))