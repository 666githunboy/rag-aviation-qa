with open("test.txt","a") as f:
    f.write("只写这一行")

print("写入完成")

with open("test.txt","r") as f:
    content=f.read()

print(content)