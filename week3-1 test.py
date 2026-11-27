import os
folder=r"D:\VS CODE\VS CODE 项目\data"
print([f for f in os.listdir(folder) if f.lower().endswith(".pdf")])