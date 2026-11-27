ata_map={29=["液压系统"],
         32=["起落架系统"],
         21=["空调系统"]
}
def get_system(ata,ataname):
    for ata_map in ata:
        if ata==29:
            return(ataname[0])
        print(ataname)
        elif ata==32:
             return(ataname[1])
        print(ataname)
        elif ata==21:
            return(ataname[2])
        print(ataname)
    else:
        print("未知系统")
get_system(29)
get_system(32)
get_system(99)