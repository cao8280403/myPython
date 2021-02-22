import clr
import time

clr.AddReference("D://OpenHardwareMonitorLib.dll")  # 加载C#的库这个库网上可以下载

from OpenHardwareMonitor.Hardware import Computer

computer_tmp = Computer()  # 实例这这个类

computer_tmp.CPUEnabled = True
computer_tmp.GPUEnabled = True  # 获取GPU温度时用
computer_tmp.HDDEnabled = True
computer_tmp.RAMEnabled = True  # 获取内存温度时用

computer_tmp.Open()

print(computer_tmp.Hardware[0].Identifier)
print(computer_tmp.Hardware[0].Sensors)
while True:
    for a in range(0, len(computer_tmp.Hardware[0].Sensors)):
        # print computer_tmp.Hardware[0].Sensors[a].Identifier
        if str(computer_tmp.Hardware[0].Sensors[a].Identifier) == "/intelcpu/0/temperature/4":
            print(computer_tmp.Hardware[0].Sensors[a].Value)
            computer_tmp.Hardware[0].Update()
    time.sleep(1)