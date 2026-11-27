import os
from pypdf import PdfReader

folder=r"D:\VS CODE\VS CODE 项目\data"

pdf_files=[f for f in os.listdir(folder)if f.lower().endswith(".pdf")]
print("找到的PDF文件:")
for f in pdf_files:
    print("-",f)

if pdf_files:
    first_pdf=os.path.join(folder,pdf_files[0])
    reader=PdfReader(first_pdf)
    print("\n打开文件:",pdf_files[0])
    print("总页数:",len(reader.pages))
    for page_num in [10,50,100]:
        text=reader.pages[page_num].extract_text()or""
        print(f"\n第{page_num+1}页字符：",len(text))
        print(text[:200])
else:
    print("这个文件夹里没有PDF文件,请检查路径。")