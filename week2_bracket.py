def show_system(ata,name):
    print("ATA",ata,"对应系统",name)

ata_list=[21,24,29,32]
system_dict={
    "ATA29":"液压系统",
    "ATA32":"起落架系统"
}

print(ata_list[2])
print(system_dict["ATA32"])

show_system(29,system_dict["ATA29"])
show_system(32,system_dict["ATA32"])