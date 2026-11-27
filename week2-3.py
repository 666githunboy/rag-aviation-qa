system_dict={"ATA29":"液压系统",
             "ATA32":"起落架系统",
             "ATA21":"空调系统"}

print(system_dict["ATA29"])
print(system_dict["ATA32"])
print(len(system_dict))

system_dict["ATA24"]="电源系统"
system_dict["ATA29"]="液压系统(修订）"
print(system_dict)

print("ATA29"in system_dict)
print("ATA99"in system_dict)