ata_list=[21,24,29,32,34]
for ata in ata_list:
    if ata==29:
        print("液压系统")
    elif ata==32:
        print("起落架系统")
    else:
        print("其他系统")
count=3
while count>=1:
    print("检查倒计时：",count)
    count=count-1
print("检查完成")