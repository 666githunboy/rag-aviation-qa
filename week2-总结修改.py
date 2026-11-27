ata_map={29:"液压系统",
         32:"起落架系统",
         21:"空调系统"
}

def get_system(ata):
    if ata in ata_map:
        return ata_map[ata]
    else:
        return"未知系统"
    
ata_list=[29,21,99,32,24]
with open("ata_result.txt","w")as f:
    for ata in ata_list:
        f.write(f"{ata} {get_system(ata)}\n")
with open("ata_result.txt","r")as f:
    content=f.read()

print(content)