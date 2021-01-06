import win32api,win32con

# a = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
#获得屏幕分辨率X轴
# b = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
dm = win32api.EnumDisplaySettings(None, 0)
dm.PelsHeight = 1440
dm.PelsWidth = 1920
dm.BitsPerPel = 32
dm.DisplayFixedOutput = 0
win32api.ChangeDisplaySettings(dm, 0)